import datetime as dt
from decimal import Decimal


import pytest
import pandas as pd


from malloc.polish_bond_value.utils import bond_value


def test_bond_value_1():
    returns = pd.DataFrame([
        [dt.date(2019, 7, 1), Decimal(2.8)],
        [dt.date(2020, 7, 1), Decimal(4.65)],
        [dt.date(2021, 7, 1), Decimal(6.45)],
        [dt.date(2022, 7, 1), Decimal(15.65)],
        [dt.date(2023, 7, 1), Decimal(14.75)]        
    ], columns=["change_date", "return"])
    
    assert bond_value(returns, dt.date(2019, 7, 17), dt.date(2024, 1, 14)) == 424.05

