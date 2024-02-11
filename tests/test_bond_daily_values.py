import datetime as dt


import pytest


def test_bond_values_in_period_1(ROS0725):
    res = ROS0725.values_in_period(dt.date(2020, 7, 20), dt.date(2024, 1, 14))    

    assert res.iloc[0]["value"] == 102.72
    assert (res.loc[dt.datetime(2020, 7, 31), "value"] == 102.80)
    assert (res.loc[dt.datetime(2024, 1, 14), "value"] == 141.35)
    
    assert res.iloc[-1]["value"] == 141.35


def test_bond_values_in_period_2(OTS0722):
    res = OTS0722.values_in_period()

    assert res.index[0] == dt.datetime(2022, 4, 15)
    assert res.iloc[0]["value"] == 100.00
    assert res.loc[dt.datetime(2022, 5, 10), "value"] == 100.10
    assert res.iloc[-2]["value"] == 100.37
    assert res.iloc[-1]["value"] == 100.00


def test_out_of_range(EDO1033):
    with pytest.raises(ValueError):
        EDO1033.values_in_period(dt.date(2018, 1, 15), dt.date(2025, 8, 25))

    with pytest.raises(ValueError):
        EDO1033.values_in_period(dt.date(2023, 11, 15), dt.date(2034, 8, 25))

    with pytest.raises(ValueError):
        EDO1033.values_in_period(dt.date(2033, 11, 15), dt.date(2034, 8, 25))

    with pytest.raises(ValueError):
        EDO1033.values_in_period(dt.date(2023, 11, 11), dt.date(2023, 8, 25))

    with pytest.raises(ValueError):
        EDO1033.values_in_period(dt.date(2023, 12, 11), dt.date(2023, 11, 12))

    