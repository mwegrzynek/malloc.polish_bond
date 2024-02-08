import datetime as dt
from typing import NamedTuple
from enum import Enum


import pandas as pd
from dateutil.relativedelta import relativedelta


BondType = NamedTuple(
    "Bond", [
        ("duration", int), 
        ("period_length", int), 
        ("rates_offset", int),
        ("capitalize", bool)
    ]
)


BOND_TYPES = {
    "OTS": BondType(1, 3, 9, False),
    "ROR": BondType(12, 1, 9, False),
    "COI": BondType(4, 12, 10, False),
    "ROS": BondType(6, 12, 9, True),
    "ROD": BondType(12, 12, 9, True),
    "EDO": BondType(10, 12, 9, True),

}

class CashFlowEvent(Enum):
    """Enum class for cash flow events."""
    purchase = 1
    coupon = 2
    redemption = 3


class Bond:

    def __init__(
            self, kind: str, series: str, duration: int, 
            period_length: int, capitalize: bool,
            starting_value: float, 
            purchase_date: dt.date, rates: list[float],
            
    ):        
        self.kind = kind
        self.series = series
        self.name = kind + series
        self.period_length = period_length
        self.duration = duration
        self.capitalize = capitalize

        self.starting_value = starting_value

        self.purchase_date = purchase_date
        self.maturity_date = dt.datetime.strptime(self.name[3:], "%m%y").replace(day=self.purchase_date.day).date()
        self.nominal_purchase_date = (self.maturity_date - relativedelta(months=self.duration * self.period_length))

        if self.nominal_purchase_date != self.purchase_date:
            raise ValueError(f"Bond name {self.name} is not consistent with purchase date {purchase_date}.")
        
        self.rates = rates
        self._last_updated = None
        
    def _compute(self):
        """Compute the daily values of the bond."""
        previous_value = current_value = self.starting_value
        previous_date = current_date = self.purchase_date
                
        cf = [(self.purchase_date, CashFlowEvent.purchase, -self.starting_value)]
        dv = None

        for rate in self.rates:          
            current_date = current_date + relativedelta(months=self.period_length)                    
            period_rate = rate * self.period_length / 12
            current_value = round(current_value * (1 + period_rate), 2) 

            df = (
                pd
                .DataFrame([
                    (previous_date, previous_value),
                    (current_date, current_value)
                ], 
                columns=["date", "value"])
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
            
            if not self.capitalize:
                cf.append((current_date, CashFlowEvent.coupon, current_value - self.starting_value))
                current_value = self.starting_value
                df.iloc[-1].value = self.starting_value

            previous_date = current_date
            previous_value = current_value

            dv = df if dv is None else pd.concat([dv, df.iloc[1:]])

        cf.append((current_date, CashFlowEvent.redemption, current_value))

        self._cash_flow = (
            pd
            .DataFrame(cf, columns=["date", "event", "value"])
        )        
        
        self._daily_values = dv        
        self._last_updated = dt.date.today()        

    @property
    def daily_values(self) -> pd.DataFrame:
        """Return a dataframe with daily values."""
        if self._last_updated is None or self._last_updated < dt.today(): 
            self._compute()
        
        return self._daily_values

    def value(self, valuation_date: dt.date) -> float:        
        """Calculate the value of a bond at a valuation date"""            
        return self.daily_values.loc[
            # Convert to datetime
            pd.to_datetime(valuation_date),
            "value"
        ]

    def values_in_period(self, date_start: dt.date=None, date_end: dt.date=None) -> pd.DataFrame:
        """Returns a dataframe with daily values with param conversion and validation."""
        if date_start is None:
            date_start = self.purchase_date
        
        elif date_start < self.purchase_date:
            raise ValueError(f"Start date {date_start} is before purchase date {self.purchase_date}.")
        
        elif date_start > self.maturity_date:
            raise ValueError(f"Start date {date_start} is after maturity date {self.maturity_date}.")

        if date_end is None:
            date_end = self.maturity_date
        
        elif date_end < self.purchase_date:
            raise ValueError(f"End date {date_end} is before purchase date {self.purchase_date}.")
        
        elif date_end > self.maturity_date:
            raise ValueError(f"End date {date_end} is after maturity date {self.maturity_date}.")
        
        if date_start > date_end:
            raise ValueError(f"Start date {date_start} is after end date {date_end}.")
            
        return self.daily_values.loc[
            pd.to_datetime(date_start):pd.to_datetime(date_end)
        ].copy()
        

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
        
        return Bond(bond_kind, bond_series, bd.duration, bd.period_length, bd.capitalize, bi.iloc[0, 5], purchase_date, rates)