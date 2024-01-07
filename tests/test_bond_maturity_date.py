import pytest
import datetime as dt

from malloc.polish_bond_value.utils import bond_maturity_date

test_data = [
    ("ROS0621", dt.date(2015, 6, 17), dt.date(2021, 6, 17)),
    ("EDO1223", dt.date(2013, 6, 15), dt.date(2023, 12, 15)),
]

@pytest.mark.parametrize("bond_name, purchase_date, maturity_date", test_data)
def test_maturity_date(bond_name, purchase_date, maturity_date):
    assert bond_maturity_date(bond_name, purchase_date) == maturity_date
