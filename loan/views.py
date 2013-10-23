# Create your views here.
from django.utils import simplejson
from balance_and_dividend.models import *
from datetime import datetime, date
import calendar
from members.models import Member
from django.http import HttpResponse
from django.shortcuts import render_to_response, render
from models import *
#from dateutil.relativedelta import relativedelta

#def add_months2(sourcedate,months):
#    return sourcedate + relativedelta( months = +months )

def add_months(sourcedate,months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month / 12
    month = month % 12 + 1
    day = min(sourcedate.day,calendar.monthrange(year,month)[1])
    return date(year,month,day)

def member_loan_request(request):
    #import pdb; pdb.set_trace
    if not request.POST or not request.session["member"]:
        return render_to_response('index.html', {})
    xhr = request.POST.has_key('xhr')
    response_dict = {}
    request_amount = request.POST.get('loanAmount')
    request_amount = float(request_amount)
    member = request.session.get("member",False)
    account = request.session.get("account",False)
    account.balance = float(account.balance)
    
    today = date.today()
    delta = today - member.registration_date

    if delta.days > 120:
        if request_amount <= account.balance:
            repayment_rate =  300#member.salary / 3
            repayment_months = 4#request_amount / repayment_rate
            repayment_date = "2013-10-7"#add_months(date.today(),repayment_months)
            response_dict.update({'date': repayment_date})#.strftime("%d-%m-%Y")})
        elif request_amount > account.balance:
            if request_amount < 120000:
                loan_limit = 8*account.balance if 8*account.balance < 120000 else 120000
                if request_amount < loan_limit:
                    repayment_rate = member.salary / 3
                    repayment_months = int(request_amount / repayment_rate)
                    repayment_date = add_months(date.today(),repayment_months)
                    response_dict.update({'date': repayment_date.strftime("%d-%m-%Y") })
                else:
                    response_dict.update({'errors': 'You have exceeded your loan limit 1'})
                    loan_limit = 8*account.balance if 8*account.balance < 120000 else 120000
                    msg = 'You cannot request more than' + str(loan_limit) + Birr
                    response_dict.update({'message':msg})
            
            elif request_amount > 120000 and account.balance < 120000:
                response_dict.update({'errors': 'You have exceeded your loan limit 2'})
                loan_limit = 8*account.balance if 8*account.balance < 120000 else 120000
                msg = 'You cannot request more than' + str(loan_limit) + Birr
                response_dict.update({'message':msg}) 
            elif account.balance > 120000:
                response_dict.update({'errors': 'You have exceeded your loan limit 3'})
                loan_limit = account.balance
                response_dict.update({'loanWas': request_amount})
                msg = 'You cannot request more than ' + str(loan_limit) + ' Birr'
                response_dict.update({'message':msg})

    else:
        response_dict.update({'errors': 'You are not yet elligible to make loan requests'})
        response_dict.update({'message':'You must wait for 4 months after registration to make a loan request'})
        request_on = add_months(member.registration_date,4)
     
    if xhr:
        return HttpResponse(simplejson.dumps(response_dict), mimetype='application/json')
    return render_to_response('member-home.html', response_dict)

def request_loan_page(request):
    if "user" in request.session and request.session["user"]:
        user = request.session["user"]
        return render(request,"request-loan.html",{'user':user})
    return render_to_response('index.html')

def loan_request(request):
    if not request.POST or not request.session["member"]:
        return render_to_response('index.html', {})
    request_amount = request.POST.get('loanAmount')
    request_amount = float(request_amount)
    request_reason = request.POST.get('loanReason', False)
    member = request.session.get("member",False)
    account = request.session.get("account",False)
    account.balance = float(account.balance)

    if request_amount and request_reason:
        loan_request = Loan_Request(member=member,amount=request_amount,request_reason=request_reason,
                request_date=date.today(),accountant_approval=False,cp_vcp_approval=False,cashier_grant=False,
                is_accepted=False,is_rejected=False,is_seen=False)
        loan_request.save()
    return render_to_response('member-home.html', {'member':member})

