import pandas as pd
import numpy as np
import datetime

def home_value(price, growth_rate, term_years):
    periods = np.arange(term_years)
    value = np.fv(growth_rate, periods, 0, -price)
    return pd.Series(
        name='home_value',
        data=value,
        index=pd.date_range(start=datetime.date.today(), periods=term_years, freq='Y')
    )

def letting_cash_flow(monthly_rate, term_years, growth_rate, vacancy_rate=2/12):
    periods = np.arange(term_years)
    value = np.fv(growth_rate, periods, 0, -1) * monthly_rate * (1-vacancy_rate)
    return pd.Series(
        name='rental_income',
        data=value,
        index=pd.date_range(start=datetime.date.today(), periods=term_years, freq='Y')
    )