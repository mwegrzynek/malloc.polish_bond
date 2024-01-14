import datetime as dt
from decimal import Decimal

import pandas as pd

def bond_maturity_date(bond_name: str, purchase_date: dt.date) -> dt.date:
    """Return the maturity date of a bond."""                
    return dt.datetime.strptime(bond_name[3:], "%m%y").replace(day=purchase_date.day).date()

def bond_value(bond_returns: pd.DataFrame, purchase_date: dt.date, valuation_date: dt.date) -> Decimal:
    """Calculate the value of a bond. bond_percentages is a DataFrame with columns:
        - change_date: date of the change of the return
        - return: return of the bond in percent
    """

    start_value = Decimal(300.0)
    periods = (
        bond_returns
        .query("change_date <= @valuation_date")    
        .assign(
            current_value=start_value
        )
        .assign(            
            current_value=lambda df: (
                Decimal(100) + df["return"].shift(-1).fillna(Decimal(0))
            ) / Decimal(100) * df["current_value"].shift(-1).fillna(start_value)
        )
    )

    print(periods)