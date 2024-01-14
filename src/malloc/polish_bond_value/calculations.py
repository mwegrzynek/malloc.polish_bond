import datetime as dt


from decimal import Decimal, getcontext


import pandas as pd
from dateutil.relativedelta import relativedelta


TWO_PLACES = Decimal("0.01")


def bond_value(rates: list[float], period_length: int, purchase_date: dt.date, valuation_date: dt.date) -> float:
    """Calculate the value of a bond. Rates is a list of rates in periods, period_length is a capitalization period in months"""    
    current_value = 100
    current_date = purchase_date    

    for rate in rates:
        previous_date = current_date        
        current_date = current_date + relativedelta(months=period_length)

        if current_date > valuation_date:
            break

        current_value = round(current_value * (100 + rate) / 100, 2)
    
    # Compute last value    
    current_value = current_value + (
        current_value * rate / 100 * 
        (valuation_date - previous_date).days / (current_date - previous_date).days
    )

    return round(current_value, 2)


def bond_maturity_date(bond_name: str, purchase_date: dt.date) -> dt.date:
    """Return the maturity date of a bond."""                
    return dt.datetime.strptime(bond_name[3:], "%m%y").replace(day=purchase_date.day).date()


def bond_daily_values(rates: list[float], period_length: int, purchase_date: dt.date, date_start: dt.date, date_end) -> float:
    """Calculate the value of a bond. Rates is a list of rates in periods, period_length is a capitalization period in months"""    
    current_value = 100
    current_date = purchase_date  

    res = [(purchase_date, current_value)]    

    for rate in rates:          
        current_date = current_date + relativedelta(months=period_length)        
        current_value = round(current_value * (100 + rate) / 100, 2)    
        res.append((current_date, current_value))
    
    res = (
        pd
        .DataFrame(res, columns=["date", "value"])
        .assign(
            date=lambda df: pd.to_datetime(df["date"]),
        )
        .set_index("date")
        .resample("D")
        .interpolate("linear")
        .assign(
            value=lambda df: df["value"].round(2)        
        )
    )

    return res