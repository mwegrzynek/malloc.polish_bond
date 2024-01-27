import datetime as dt
from typing import NamedTuple


import pandas as pd
from dateutil.relativedelta import relativedelta


BondType = NamedTuple(
    "Bond", [
        ("duration", int), 
        ("period_length", int), 
        ("rates_offset", int)
    ]
)


BOND_TYPES = {
    "OTS": BondType(1, 3, 9),
    "COI": BondType(4, 12, 10),
    "ROS": BondType(6, 12, 9),
    "ROD": BondType(12, 12, 9),
    "EDO": BondType(10, 12, 9),
}


class Bond:

    def __init__(
            self, kind: str, series: str, duration: int, 
            period_length: int, starting_value: float, 
            purchase_date: dt.date, rates: list[float]
    ):        
        self.kind = kind
        self.series = series
        self.name = kind + series
        self.period_length = period_length
        self.duration = duration

        self.starting_value = starting_value

        self.purchase_date = purchase_date
        self.maturity_date = dt.datetime.strptime(self.name[3:], "%m%y").replace(day=self.purchase_date.day).date()
        self.nominal_purchase_date = (self.maturity_date - relativedelta(months=self.duration * self.period_length))

        if self.nominal_purchase_date != self.purchase_date:
            raise ValueError(f"Bond name {self.name} is not consistent with purchase date {purchase_date}.")
        
        self.rates = rates
                
    def value(self, valuation_date: dt.date) -> float:        
        """Calculate the value of a bond. Rates is a list of rates in periods, period_length is a capitalization period in months"""    
        if valuation_date < self.purchase_date:
            raise ValueError(f"Valuation date {valuation_date} is before purchase date {self.purchase_date}.")
        
        if valuation_date > self.maturity_date: 
            return 0.0

        current_value = self.starting_value
        current_date = self.purchase_date

        for rate in self.rates:
            previous_date = current_date        
            current_date = current_date + relativedelta(months=self.period_length)

            if current_date > valuation_date:
                break

            current_value = round(current_value * (1 + rate) * self.period_length / 12, 2)            

        # Compute last value    
        current_value = current_value + (
            current_value * rate * 
            (valuation_date - previous_date).days / (current_date - previous_date).days
        )

        return round(current_value, 2)

    def daily_values(self, date_start: dt.date, date_end: dt.date) -> pd.DataFrame:
        """Calculate the value of a bond. Rates is a list of rates in periods, period_length is a capitalization period in months"""    
        if date_start > date_end:
            raise ValueError(f"Start date {date_start} is after end date {date_end}.")
        
        if date_start < self.purchase_date:
            raise ValueError(f"Start date {date_start} is before purchase date {self.purchase_date}.")
        
        if date_start > self.maturity_date:
            raise ValueError(f"Start date {date_start} is after maturity date {self.maturity_date}.")

        if date_end < self.purchase_date:
            raise ValueError(f"End date {date_end} is before purchase date {self.purchase_date}.")
        
        if date_end > self.maturity_date:
            raise ValueError(f"End date {date_end} is after maturity date {self.maturity_date}.")
        
        current_value = self.starting_value
        current_date = self.purchase_date  

        res = [(self.purchase_date, current_value)]    

        for rate in self.rates:          
            current_date = current_date + relativedelta(months=self.period_length)        
            current_value = round(current_value * (1 + rate) * self.period_length / 12, 2)    
            res.append((current_date, current_value))
        
        res = (
            pd
            .DataFrame(res, columns=["date", "value"])
            .assign(
                date=lambda df: pd.to_datetime(df["date"]),
            )
            .set_index("date")
            .resample("D")
            .interpolate("linear")
            .assign(
                value=lambda df: df["value"].round(2)        
            )
        )

        return res
    

class BondMaker:
          
    def __init__(self, data_url: str="https://api.dane.gov.pl/resources/53432,sprzedaz-obligacji-detalicznych/file"):
        """Initialize the factory with data from the given URL."""
        self.bond_info = pd.read_excel(data_url, sheet_name=None)
    
    def __call__(self, bond_name: str, purchase_date: dt.date) -> Bond:
        """Calculate the value of a bond between two dates."""
        bond_kind = bond_name[:3]        
        bond_series = bond_name[3:]

        try:
            bd = BOND_TYPES[bond_kind]
        except KeyError:
            raise ValueError(f"Bond kind {bond_kind} is not supported.")
        
        bi = self.bond_info[bond_kind].query("Seria == @bond_name")
        rates = [rt for _, rt in bi.iloc[0, bd.rates_offset:bd.rates_offset + bd.duration].items()]
        
        return Bond(bond_kind, bond_series, bd.duration, bd.period_length, bi.iloc[0, 5], purchase_date, rates)