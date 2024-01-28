import datetime as dt


def test_bond_daily_values(ROS0725):
    res = ROS0725.daily_values(dt.date(2020, 7, 20), dt.date(2024, 1, 14))

    assert res.iloc[0]["value"] == 100.0
    assert res.loc[dt.datetime(2020, 7, 31), "value"] == 102.80
    assert res.loc[dt.datetime(2024, 1, 14), "value"] == 141.35
    
    assert res.iloc[-1]["value"] == 141.35