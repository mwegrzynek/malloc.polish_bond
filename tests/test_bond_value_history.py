from datetime import date
import pytest


def test_not_existing_bond(calc):
    """Test that a non-existing bond raises a KeyError."""
    with pytest.raises(KeyError):
        calc.value_history("XXX0000", date(2023, 12, 31))

# def test_sample_value_history_1(calc):    
#     assert calc.value_history("COI0924", "2023-11-30", "2023-12-31") == 1000

def test_sample_value_history_2(calc):    
    assert calc.value_history("ROS0725", date(2019, 7, 31)) == 1234