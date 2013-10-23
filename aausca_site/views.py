from django.http import HttpResponse
from django.shortcuts import render,render_to_response
from members.models import Member
from balance_and_dividend.models import *
from loan.models import *
from datetime import *

def member_login(request):
	errors = []
	if 'memberIdEmail' in request.POST and request.POST['memberIdEmail']:
		user_id_email = request.POST['memberIdEmail']
	else:
		errors.append("You forgot to submit your member id!")
	if 'password' in request.POST and request.POST['password']:
		password = request.POST['password']
	else:
		errors.append("You forgot to submit your password!")
	if not errors:

		user = None
		member = None
		account = None
		loan_request = None
		loan_disbursement = None
		loan_renewal = None
		loan_extenstion = None
		guarantee = None

		try:
			user = User.objects.get(user_id=user_id_email, password=password)
		except User.DoesNotExist:
			errors.append("There is no such user")
		
		if user:
			try:
				member = Member.objects.get(member_id=user.user_id)
			except Member.DoesNotExist:
				errors.append("The member's profile of the user is unavailable")
		
		if member:
			try:
				account = Savings_Account.objects.get(member=member)
			except Savings_Account.DoesNotExist:
				errors.append("The member's account information of the user is unavailable")
		
		if member:
			try:
				loan_request = Loan_Request.objects.filter(member=member)
			except Loan_Request.DoesNotExist:
				errors.append("The member has no loan request history")

		if member:
			try:
				loan_disbursement = Loan_Disbursement.objects.filter(member=member)
			except Loan_Disbursement.DoesNotExist:
				errors.append("The member has no loan disbursement history")

		if member:
			try:
				loan_renewal = Loan_Renewal.objects.filter(member=member)
			except Loan_Renewal.DoesNotExist:
				errors.append("The member has no loan renewal history")

		if member:
			try:
				loan_extenstion = Loan_Extension.objects.filter(member=member)
			except Loan_Extension.DoesNotExist:
				errors.append("The member has no loan extension history")

		if member:
			try:
				guarantee = Guarantee.objects.filter(member=member)
			except Guarantee.DoesNotExist:
				errors.append("The member has no guarantee history")

		if member:
			request.session["member"] = member
			request.session["account"] = account
			return render(request,"member-home.html",{'member':member,'account':account,'loan_request':loan_request,'loan_disbursement':loan_disbursement,'loan_renewal':loan_renewal,'loan_extenstion':loan_extenstion,'guarantee':guarantee})			 
		else:
			return render(request,'index.html')
	else:
		return render(request,'index.html')

def member_home(request):
	if "member" not in request.session:
		return render(request,'index.html')
	return render(request,"member-home.html")
def register_page(request):
	return render(request,'apply.html')
def login_page(request):
	return render(request,'login.html')
def home_page(request):
	return render(request,'index.html')
def login(request):
	errors = []
	if 'userIdEmail' in request.POST and request.POST['userIdEmail']:
		user_id_email = request.POST['userIdEmail']
		if user_id_email.startswith("mem"):
			errors.append("You are not an administrator!")
		else:
			request.session["user"] = user_id_email
	else:
		errors.append("You forgot to submit your member id!")
	if 'password' in request.POST and request.POST['password']:
		password = request.POST['password']
	else:
		errors.append("You forgot to submit your password!")
	
	if not errors:
		try:
			user = User.objects.get(user_id=user_id_email, password=password)
		except User.DoesNotExist:
			errors.append("There is no such user")
			return render(request,"index.html",{'errors':errors})
		else:
			if user.user_type == 1:
				return render(request,"clerk-home.html",{'user':user_id_email})
			elif user.user_type == 2:
				return render(request,"accountant-home.html",{'user':user_id_email})		 
	else:
		return render(request,"login.html",{'errors':errors})

def apply(request):
	errors = []
	if 'inputName' in request.POST and request.POST['inputName']:
		member_name = request.POST['inputName']
	else:
		errors.append("You Forgot to submit your first name!")

	if 'inputFathersName' in request.POST and request.POST['inputFathersName']:
		member_father_name = request.POST['inputFathersName']
	else:
		errors.append("You forgot to submit your father's name!")

	if 'inputGrandFathersName' in request.POST and request.POST['inputGrandFathersName']:
		member_grand_father_name = request.POST['inputGrandFathersName']
	else:
		errors.append("You Forgot to submit your grand father's name!")

	if 'inputSex' in request.POST and request.POST['inputSex']:
		member_sex = request.POST['inputSex']
	else:
		errors.append("You forgot to submit your sex!")

	if 'inputBirthDay' in request.POST and request.POST['inputBirthDay']:
		member_birth_day = int(request.POST['inputBirthDay'])
	else:
		errors.append("You forgot to submit your birth day!")

	if 'inputBirthMonth' in request.POST and request.POST['inputBirthMonth']:
		member_birth_month = int(request.POST['inputBirthMonth'])
	else:
		errors.append("You forgot to submit your birth month!")

	if 'inputBirthYear' in request.POST and request.POST['inputBirthYear']:
		member_birth_year = int(request.POST['inputBirthYear'])
	else:
		errors.append("You forgot to submit your birth year!")

	if 'inputSubcity' in request.POST and request.POST['inputSubcity']:
		member_subcity = request.POST['inputSubcity']
	else:
		errors.append("You forgot to submit your subcity!")

	if 'inputWereda' in request.POST and request.POST['inputWereda']:
		member_wereda = request.POST['inputWereda']
	else:
		errors.append("You forgot to submit your wereda")

	if 'inputHouseNumber' in request.POST and request.POST['inputHouseNumber']:
		member_house_number = request.POST['inputHouseNumber']
	else:
		errors.append("You forgot to submit your house number!")

	if 'inputHousePhoneNumber' in request.POST and request.POST['inputHousePhoneNumber']:
		member_house_phone_number = request.POST['inputHousePhoneNumber']
	
	if 'inputOfficePhoneNumber' in request.POST and request.POST['inputOfficePhoneNumber']:
		member_office_phone_number = request.POST['inputOfficePhoneNumber']
	else:
		errors.append("You forgot to submit your office phone number!")

	if 'inputCellPhoneNumber' in request.POST and request.POST['inputCellPhoneNumber']:
		member_cell_phone_number = request.POST['inputCellPhoneNumber']
	else:
		errors.append("You forgot to submit your cell phone number!")

	if 'inputPOBox' in request.POST and request.POST['inputPOBox']:
		member_pobox = request.POST['inputPOBox']

	if 'inputFaculty' in request.POST and request.POST['inputFaculty']:
		member_faculty = request.POST['inputFaculty']
	else:
		errors.append("You forgot to submit your faculty!")

	if 'inputCampus' in request.POST and request.POST['inputCampus']:
		member_campus = request.POST['inputCampus']
	else:
		errors.append("You forgot to submit your campus!")

	if 'inputDepartment' in request.POST and request.POST['inputDepartment']:
		member_department = request.POST['inputDepartment']
	else:
		errors.append("You forgot to submit your department")

	if 'inputEmploymentType' in request.POST and request.POST['inputEmploymentType']:
		member_employement_type = request.POST['inputEmploymentType']
	else:
		errors.append("You forgot to submit your employment type!")

	if 'inputSalary' in request.POST and request.POST['inputSalary']:
		member_salary = request.POST['inputSalary']
	else:
		errors.append("You forgot to submit your salary!")

	if 'inputSavingsPercentage' in request.POST and request.POST['inputSavingsPercentage']:
		member_savings_percentage = request.POST['inputSavingsPercentage']
	else:
		errors.append("You forgot to submit your savings percentage!")

	if 'inputEmail' in request.POST and request.POST['inputEmail']:
		member_email = request.POST['inputEmail']
	else:
		errors.append("You forgot to submit your e-mail!")
	if 'inputPassword' in request.POST and request.POST['inputPassword'] and 'inputRetypePassword' in request.POST and request.POST['inputRetypePassword']:
		if request.POST['inputPassword'] == request.POST['inputRetypePassword']:
			member_password = request.POST['inputPassword']
		else:
			errors.append("The password fields you submitted dont match!")
	else:
		errors.append("You forgot to complete the password fields!")

	if not errors:
		member = Member(member_id="mem-"+str(Member.objects.latest('id').id+1),first_name=member_name, father_name=member_father_name, 
					grand_father_name=member_grand_father_name, sex=member_sex,
					birth_date=date(member_birth_year,member_birth_month,member_birth_day),subcity=member_subcity,
					wereda=member_wereda,house_number=member_house_number,house_phone_number=member_house_phone_number,
					office_phone_number=member_office_phone_number,cell_phone_number=member_cell_phone_number,POBox=member_pobox,
					campus=member_campus,faculty=member_faculty,department=member_department,employment_type=member_employement_type,salary=member_salary,
					email=member_email,is_registered=False,application_date=datetime.now().strftime("%Y-%m-%d"),registration_date=datetime.now().strftime("%Y-%m-%d"))
		user = User(user_id=member.member_id,user_type=0,email=member_email,password=member_password)
		user.save()
		member.save()
		account = Savings_Account(id=Savings_Account.objects.latest('id').id+1,account_id="acc-"+str(Savings_Account.objects.latest('id').id+1),
				member=member,interest_rate=4.8,balance=0,creation_date=datetime.now().strftime("%Y-%m-%d"),
				savings_percentage=member_savings_percentage,is_seen=False)
		account.save()
		"""
		"""
		return render(request,"congratulations.html",{'name':"desk clerk",'member':member_name+" "+member_father_name,'date':datetime.now().strftime("%Y-%m-%d")})
	else:
		return render(request,"apply.html",{'errors':errors})# Create your views here.

def register_member(request):
	if "user" not in request.session:
		return render(request,"index.html")
	user = request.session["user"]
	return render(request,"registration.html",{'user':user})


def view_profile(request):
	if "user" not in request.session:
		return render(request,"index.html")
	user = request.session["user"]
	return render(request,"view-profile.html",{'user':user})

def edit_profile(request):
	if "user" not in request.session:
		return render(request,"index.html")
	user = request.session["user"]
	return render(request,"edit-profile.html",{'user':user})

def extend_loan(request):
	if "user" in request.session and request.session["user"]:
		user = request.session["user"]
		return render(request,"extend-loan.html",{'user':user})
	return render_to_response('index.html')

def transactions(request):
	if "user" in request.session and request.session["user"]:
		user = request.session["user"]
		return render(request,"transactions.html",{'user':user})
	return render_to_response('index.html')

def logout(request):
	request.session.flush()
	return render(request,'login.html')

def member_logout(request):
	request.session.flush()
	return render(request,'index.html')

def member_edit_profile(request):
	if "member" in request.session and request.session["member"]:
		mem = request.session["member"]

		try:
			member = Member.objects.get(member_id=mem.member_id)
		except Member.DoesNotExist:
			return render(request,"member-home.html",{'message':'Failed to update your profile'})

		if 'inputHouseNumber' in request.POST and request.POST['inputHouseNumber']:
			house_number = request.POST['inputHouseNumber']
			member.house_number = house_number
		
		if 'inputSubcity' in request.POST and request.POST['inputSubcity']:
			subcity = request.POST['inputSubcity']
			member.subcity = subcity

		if 'inputPOBox' in request.POST and request.POST['inputPOBox']:
			POBox = request.POST['inputPOBox']
			member.POBox = POBox

		if 'inputWereda' in request.POST and request.POST['inputWereda']:
			wereda = request.POST['inputWereda']
			member.wereda = wereda

		if 'inputOfficePhoneNumber' in request.POST and request.POST['inputOfficePhoneNumber']:
			office_phone_number = request.POST['inputOfficePhoneNumber']
			member.office_phone_number = office_phone_number

		if 'inputCellPhoneNumber' in request.POST and request.POST['inputCellPhoneNumber']:
			cell_phone_number = request.POST['inputCellPhoneNumber']
			member.cell_phone_number = cell_phone_number

		if 'inputFaculty' in request.POST and request.POST['inputFaculty']:
			faculty = request.POST['inputFaculty']
			member.faculty = faculty

		if 'inputDepartment' in request.POST and request.POST['inputDepartment']:
			department = request.POST['inputDepartment']
			member.department = department		
		

		member.save()
		member = Member.objects.get(member_id=member.member_id)

		if member:
			try:
				account = Savings_Account.objects.get(member=member)
			except Savings_Account.DoesNotExist:
				errors.append("The member's account information of the user is unavailable")
		
		if member:
			try:
				loan_request = Loan_Request.objects.filter(member=member)
			except Loan_Request.DoesNotExist:
				errors.append("The member has no loan request history")

		if member:
			try:
				loan_disbursement = Loan_Disbursement.objects.filter(member=member)
			except Loan_Disbursement.DoesNotExist:
				errors.append("The member has no loan disbursement history")

		if member:
			try:
				loan_renewal = Loan_Renewal.objects.filter(member=member)
			except Loan_Renewal.DoesNotExist:
				errors.append("The member has no loan renewal history")

		if member:
			try:
				loan_extenstion = Loan_Extension.objects.filter(member=member)
			except Loan_Extension.DoesNotExist:
				errors.append("The member has no loan extension history")

		if member:
			try:
				guarantee = Guarantee.objects.filter(member=member)
			except Guarantee.DoesNotExist:
				errors.append("The member has no guarantee history")

		return render(request,"member-home.html",{'member':member,'account':account,'loan_request':loan_request,'loan_disbursement':loan_disbursement,'loan_renewal':loan_renewal,'loan_extenstion':loan_extenstion,'guarantee':guarantee})			 
		
	else:
		render(request,"index.html")

def member_loan_request(request):
	if "member" in request.session and request.session["member"]:
		member = request.session["member"]
		erros = []
		if "loanAmount" in request.POST and request.POST["loanAmount"]:
			loan_amount = request.POST["loanAmount"]
		else:
			errors.append('You have not specified a loan amount')

		if "loanReason" in request.POST and request.POST["loanReason"]:
			loan_reason = request.POST["loanReason"]
		else:
			errors.append('You have not specified a loan reason')

		if not errors:
			loan_request = Loan_Request(member=member,amount=loan_amount,reason=loan_reason,request_date=datetime.now(),
				accountant_approval=False,cp_vcp_approval=False,cashier_grant=False,is_accepted=False,is_rejected=False,
				is_seen=False)
			loan_request.save()
			return render(request,"member-home.html",{'message':'You have made a loan request'})						

		return render(request,"member-home.html")
	return render_to_response('index.html')


