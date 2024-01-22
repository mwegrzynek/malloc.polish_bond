import os
import datetime as dt


import pytest


DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


@pytest.fixture(scope="session")
def bond_factory():
    from malloc.polish_bond_value.bond import BondFactory
    data_path = os.path.join(DATA_DIR, "Dane_dotyczace_obligacji_detalicznych.xls")
    return BondFactory(data_path)


@pytest.fixture()
def ROS0725(bond_factory):
    return bond_factory("ROS0725", dt.date(2019, 7, 31))


@pytest.fixture()
def ROS0328(bond_factory):
    return bond_factory("ROS0328", dt.date(2022, 3, 30))


@pytest.fixture()
def EDO1033(bond_factory):
    return bond_factory("EDO1033", dt.date(2023, 10, 30))