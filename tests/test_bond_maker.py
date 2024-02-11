import datetime as dt


import pytest


def test_unknown_bond_type(bond_maker):
    with pytest.raises(ValueError):        
        bnd = bond_maker("XYZ1234", dt.date(2022, 1, 15))


def test_inconsistent_creation_date(bond_maker):
    
    with pytest.raises(ValueError):
        bnd = bond_maker("OTS0722", dt.date(2022, 1, 15))

    with pytest.raises(ValueError):
        bnd = bond_maker("OTS0722", dt.date(2024, 1, 15))

