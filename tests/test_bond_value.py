import datetime as dt


import pytest


@pytest.mark.parametrize(
        "bond,val_date,cnt,value", [
            (pytest.lazy_fixture("ROS0725"), dt.date(2024, 1, 14), 3, 424.05),
            (pytest.lazy_fixture("ROS0328"), dt.date(2024, 1, 22), 25, 2938.25),
            (pytest.lazy_fixture("EDO1033"), dt.date(2024, 1, 22), 155, 15757.30),
            (pytest.lazy_fixture("OTS0119"), dt.date(2018, 12, 31), 1, 100.37),
            (pytest.lazy_fixture("OTS0324"), dt.date(2024, 2, 29), 1, 100.75),
            (pytest.lazy_fixture("OTS0722"), dt.date(2022, 7, 14), 1, 100.37),
            (pytest.lazy_fixture("ROR0124"), dt.date(2023, 2, 13), 1, 100.54),
            (pytest.lazy_fixture("TOS0626"), dt.date(2026, 6, 1), 1, 121.99)
        ]
)
def test_bond_value(bond, val_date, cnt, value):        
    assert bond.value(val_date) * cnt == pytest.approx(value, 0.001)

def test_out_of_range_date_1(ROS0725):
    with pytest.raises(KeyError):
        ROS0725.value(dt.date(2018, 1, 15))

    with pytest.raises(KeyError):
        ROS0725.value(dt.date(2025, 8, 25))