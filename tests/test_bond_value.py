import datetime as dt


def test_bond_value_1(ROS0725):    
    assert abs(ROS0725.value(dt.date(2024, 1, 14))) * 3 - 424.05 < 0.01


def test_bond_value_2(ROS0328):    
    assert abs(ROS0328.value(dt.date(2024, 1, 22)) * 25 - 2938.25) < 0.01


def test_bond_value_3(EDO1033):    
    assert abs(EDO1033.value(dt.date(2024, 1, 22)) * 155 - 15757.30) < 0.01
