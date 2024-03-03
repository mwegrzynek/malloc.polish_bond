import datetime as dt
from typing import NamedTuple
from enum import Enum


from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd
from pydantic import BaseModel, PositiveInt, PositiveFloat, computed_field, model_validator, ConfigDict
import requests


BondType = NamedTuple(
    "Bond", [
        ("number_of_periods", int), 
        ("period_length", int), 
        ("capitalize", bool),
        ("rates_offset", int),
        ("constant_rate", bool)
    ]
)


BOND_TYPES = {
    "OTS": BondType(1, 3, False, 9, False),
    "ROR": BondType(12, 1, False, 9, False),
    "DOR": BondType(24, 1, False, 9, False),
    "TOS": BondType(3, 12, True, 9, True),
    "COI": BondType(4, 12, False, 9, False),
    "EDO": BondType(10, 12, True, 9, False),
    "ROS": BondType(6, 12, True, 9, False),
    "ROD": BondType(12, 12, True, 9, False),
    "TOZ": BondType(6, 6, False, 9, False),    
}

class CashFlowEvent(Enum):
    """Enum class for cash flow events."""
    purchase = 1
    coupon = 2
    redemption = 3


class Bond(BaseModel):
    kind: str
    series: str    
    number_of_periods: PositiveInt
    period_length: PositiveInt
    capitalize: bool
    starting_value: PositiveFloat
    purchase_date: dt.date
    rates: list[float | None]
    _last_updated: dt.date = None
    
    @computed_field
    def name(self) -> str:
        return self.kind + self.series
    
    @computed_field
    def maturity_date(self) -> dt.date:
        return dt.datetime.strptime(self.name[3:], "%m%y").replace(day=self.purchase_date.day).date()

    @computed_field
    def nominal_purchase_date(self) -> dt.date:
        return self.maturity_date - relativedelta(months=self.number_of_periods * self.period_length)
    
    @computed_field
    def current_value(self) -> float:        
        return self.daily_values.loc[
            dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0), 
            "value"
        ]

    @model_validator(mode="after")
    def check_purchase_dates(self) -> 'Bond':
        if self.nominal_purchase_date != self.purchase_date:
            raise ValueError(f"Bond name {self.name} is not consistent with purchase date {self.purchase_date}.")
        return self
        
    def _compute(self):
        """Compute the daily values of the bond."""
        previous_value = current_value = self.starting_value
        previous_date = current_date = self.purchase_date
                
        cf = [(self.purchase_date, CashFlowEvent.purchase, -self.starting_value)]
        dv = None

        for rate in self.rates:
            
            if rate is None:
                break

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
            .set_index("date")
        )        
        
        self._daily_values = dv        
        self._last_updated = dt.date.today()        

    @property
    def daily_values(self) -> pd.DataFrame:
        """Return a dataframe with daily values."""
        if self._last_updated is None or self._last_updated < dt.date.today(): 
            self._compute()
        
        return self._daily_values

    @property
    def cash_flow(self) -> pd.DataFrame:
        """Return a dataframe with cash flow events."""
        if self._last_updated is None or self._last_updated < dt.date.today(): 
            self._compute()
        
        return self._cash_flow

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

    def __init__(self, data_url: str):
        """Initialize the factory with data from the given URL"""        
        self.data_url = data_url
        self.bond_info = pd.read_excel(self.data_url, sheet_name=None)

    def __call__(self, bond_name: str, purchase_date: dt.date) -> Bond:
        """Return a bond object from name and purchase date."""
        bond_kind = bond_name[:3]        
        bond_series = bond_name[3:]

        try:
            bd = BOND_TYPES[bond_kind]
        except KeyError:
            raise ValueError(f"Bond kind {bond_kind} is not supported.")
        
        bi = (
            self
            .bond_info[bond_kind]
            .query("Seria == @bond_name")
            .replace([np.nan], [None])
        )
        if bd.constant_rate:
            rates = [bi.iloc[0, bd.rates_offset]] * bd.number_of_periods
        else:
            rates = [rt for _, rt in bi.iloc[0, bd.rates_offset:bd.rates_offset + bd.number_of_periods].items()]
        
        return Bond(
            kind=bond_kind, 
            series=bond_series, 
            number_of_periods=bd.number_of_periods, 
            period_length=bd.period_length, 
            capitalize=bd.capitalize, 
            starting_value=bi.iloc[0, 5], 
            purchase_date=purchase_date, 
            rates=rates
        )