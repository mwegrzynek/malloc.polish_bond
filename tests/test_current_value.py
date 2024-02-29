import datetime as dt


import pytest


def test_bond_values_in_period_1(ROS0725):
    res = ROS0725.current_value

    assert res > 0