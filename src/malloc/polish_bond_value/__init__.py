import datetime as dt

import pandas as pd
from dateutil.relativedelta import relativedelta


__version__ = "0.1.0"

BOND_MATURITIES = {
    "COI": 4 * 12,
    "ROS": 6 * 12
}


class Calculator:
    
    def __init__(self, data_url: str="https://api.dane.gov.pl/resources/53432,sprzedaz-obligacji-detalicznych/file"):
        """Initialize the calculator with data from the given URL."""
        self.bond_info = pd.read_excel(data_url, sheet_name=None)


    def _ROS(self, bi: pd.DataFrame, periods) -> pd.DataFrame:
        """Calculate the value of a ROS bond."""
        price = bi.iloc[0, 5] 
        current_value = price
        current_interest = 0.0

        result = []               

        for idx, period in enumerate(periods):
            result.append([period, current_interest, current_value, current_value * 3])
            current_interest = round(current_value * bi.iloc[0, -8 + idx], 2)
            current_value = round(current_value + current_interest, 2)

        print("\n", result)
        return result
        
    def value_history(self, bond_name: str, purchase_date: dt.date, maturity_date: dt.date = None) -> pd.DataFrame:
        """Calculate the value of a bond between two dates."""
        bond_kind = bond_name[:3]        
        
        bi = self.bond_info[bond_kind].query("Seria == @bond_name")

        bond_series = bond_name[3:]
        bond_maturity_date = dt.datetime.strptime(bond_series, "%m%y")

        if maturity_date is None:
            maturity_date = bond_maturity_date

        bond_nominal_purchase_date = (bond_maturity_date - relativedelta(months=BOND_MATURITIES[bond_kind])).date()

        if bond_nominal_purchase_date != purchase_date.replace(day=1):
            raise ValueError(f"Bond series {bond_series} is not consistent with purchase date {purchase_date}.")
        
        # Calculate amount of periods between purchase date and maturity date
        periods = [purchase_date + relativedelta(years=period) for period in range(int(maturity_date.year - purchase_date.year) + 1)]

        result = getattr(self, f"_{bond_kind}")(bi, periods)
        return result        
        

