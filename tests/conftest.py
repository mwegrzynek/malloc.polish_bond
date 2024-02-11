import os
import datetime as dt


import pytest


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture(scope="session")
def bond_maker():
    from malloc.polish_bond_value.bond import BondMaker
    data_path = os.path.join(DATA_DIR, "Dane_dotyczace_obligacji_detalicznych.xls")
    return BondMaker(data_path)


@pytest.fixture()
def ROS0725(bond_maker):
    return bond_maker("ROS0725", dt.date(2019, 7, 31))


@pytest.fixture()
def ROS0328(bond_maker):
    return bond_maker("ROS0328", dt.date(2022, 3, 30))


@pytest.fixture()
def EDO1033(bond_maker):
    return bond_maker("EDO1033", dt.date(2023, 10, 30))

@pytest.fixture()
def OTS0119(bond_maker):
    return bond_maker("OTS0119", dt.date(2018, 10, 1))

@pytest.fixture()
def OTS0324(bond_maker):
    return bond_maker("OTS0324", dt.date(2023, 12, 1))

@pytest.fixture()
def OTS0722(bond_maker):
    return bond_maker("OTS0722", dt.date(2022, 4, 15))

@pytest.fixture()
def COI0924(bond_maker):
    return bond_maker("COI0924", dt.date(2020, 9, 14))