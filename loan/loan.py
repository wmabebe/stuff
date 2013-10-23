from decimal import *
import math
from datetime import *
from dateutil.relativedelta import relativedelta

def calculate_repayment_date(amount,repayment_rate):
	time = int(math.ceil(amount/repayment_rate))
	return_date = date.today() + relativedelta( months = +time )
	return return_date
	
def calcualte_total_loan_amount(loan,interest_rate,repayment_rate):
	time = Decimal(math.ceil(loan/repayment_rate))
	interest = Decimal((Decimal(interest_rate) / 1200 * loan) * time)
	amount = Decimal(loan + interest)
	return amount,interest
