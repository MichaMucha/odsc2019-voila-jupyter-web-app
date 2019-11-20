import pandas as pd
import numpy as np
import datetime

def mortgage(price:int, downpayment:int, rate:float, term_years:int, interest_only=False) -> pd.DataFrame:
    
    principal = price - downpayment
    rate = rate / 12
    term = term_years * 12
    periods = np.arange(term) + 1
    
    if not interest_only:
        full_payments = np.pmt(rate, term, principal) * np.ones_like(periods)
        principal_payments = np.ppmt(rate, periods, term, principal)
        interest_payments = np.ipmt(rate, periods, term, principal)
    else:
        full_payments = (principal * rate) * -np.ones_like(periods)
        principal_payments = np.zeros_like(periods)
        interest_payments = full_payments
        
    debt_balance = (principal + principal_payments.cumsum()).round(2)
    
    return pd.DataFrame(
        data=np.array([debt_balance, full_payments, principal_payments, interest_payments]).T,
        columns='debt_balance, full_payments, principal_payments, interest_payments'.split(', '),
        index=pd.date_range(start=datetime.date.today(), periods=term, freq='M')
    )