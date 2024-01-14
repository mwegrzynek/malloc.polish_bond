import datetime as dt
from decimal import Decimal


import pytest
import pandas as pd


from malloc.polish_bond_value.calculations import bond_value, bond_value_decimal


def test_bond_value_1():
    returns = [2.8, 4.65, 6.45, 15.65, 14.75]    
    assert abs(bond_value(returns, 12, dt.date(2019, 7, 31), dt.date(2024, 1, 14)) * 3 - 424.05) < 0.01


def test_bond_value_2():
    returns = [2.0, 18.70]        
    assert abs(bond_value(returns, 12, dt.date(2022, 3, 30), dt.date(2024, 1, 14)) * 25 - 2927.75) < 0.01


def test_bond_value_3():
    returns = [7.25]        
    assert abs(bond_value(returns, 12, dt.date(2023, 10, 30), dt.date(2024, 1, 14)) * 155 - 15734.05) < 0.01
