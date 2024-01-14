import datetime as dt
from decimal import Decimal


import pytest
import pandas as pd


from malloc.polish_bond_value.utils import bond_value, bond_value_decimal


def test_bond_value_decimal():
    returns = [
        Decimal("2.8"),
        Decimal("4.65"),
        Decimal("6.45"),
        Decimal("15.65"),
        Decimal("14.75")        
    ]
    
    assert bond_value_decimal(returns, 12, dt.date(2019, 7, 31), dt.date(2024, 1, 14)) * 3 == Decimal("424.05")


def test_bond_value():
    returns = [2.8, 4.65, 6.45, 15.65, 14.75]    
    assert abs(bond_value(returns, 12, dt.date(2019, 7, 31), dt.date(2024, 1, 14)) * 3 - 424.05) < 0.01

