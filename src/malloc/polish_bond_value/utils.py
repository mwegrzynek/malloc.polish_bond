import datetime as dt

def bond_maturity_date(bond_name: str, purchase_date: dt.date) -> dt.date:
    """Return the maturity date of a bond."""                
    return dt.datetime.strptime(bond_name[3:], "%m%y").replace(day=purchase_date.day).date()