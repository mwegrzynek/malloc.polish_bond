import os

import pytest

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")

@pytest.fixture(scope="session")
def calc():
    from malloc.polish_bond_value import Calculator
    data = open(os.path.join(DATA_DIR, "Dane_dotyczace_obligacji_detalicznych.xls"), "rb")
    return Calculator(data)