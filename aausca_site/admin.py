from django.contrib import admin
from django.contrib import messages
from members.models import *
from balance_and_dividend.models import *
from loan.models import *
from loan.loan import *
from datetime import *
from constants.models import *
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from django.db.models import F
from math import *
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from transactions.models import *
from django.forms.models import inlineformset_factory

class MemberAdmin(admin.ModelAdmin):
	search_fields = ['first_name','father_name','grand_father_name','member_id']
	list_filter = ['registration_date','is_registered','sex','employment_type','subcity','campus','department']
	list_display = ['display_photo','member_id','first_name','father_name','grand_father_name','registration_date','salary','campus','cell_phone_number','is_registered']
	ordering = ['first_name','father_name','grand_father_name','registration_date']
	list_display_links = ['member_id']
	list_per_page = 20
	
	def register(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name="chair").count():
			for m in queryset:
				if not m.is_registered:
					try:
						if not Savings_Account.objects.filter(member=m).exists():						
							constant = Constant.objects.get(id=1)
							"""
							delta = date(2013,8,2) - m.application_date
							months = int(ceil(delta.days / 30))
							monthly_principal = (m.savings_percentage / 100) * m.salary
							monthly_interest = monthly_principal * constant.savings_interest_rate / 100
							monthly_amount = monthly_principal + monthly_interest
							total_principal = months * monthly_principal
							total_interest = months * monthly_interest
							total_balance = months * monthly_amount
							"""
							account = Savings_Account(member=m,balance=0,savings_percentage=m.savings_percentage,interest_rate=constant.savings_interest_rate,creation_date=date.today())
							account.save()
					except ObjectDoesNotExist:
						messages.warning(request,"The member account already exists")
					rows_updated += queryset.filter(id=m.id).update(registration_date=date.today(),is_registered=True)
		if rows_updated == 1:
			message_bit = "1 member was"
			self.message_user(request, "%s successfully marked as registered." % message_bit)
		else:
			message_bit = "%s members were" % rows_updated
			self.message_user(request, "%s successfully marked as registered." % message_bit)
	register.short_description = "Mark selected members as registered"
	
	def unregister(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name="chair").count():
			for m in queryset:
				Savings_Account.objects.filter(member=m).delete()
			queryset.filter().update(is_registered=False)
	unregister.short_description = "Mark the following members as unregistered"
	
	actions = [register,unregister]
	
	def get_actions(self, request):
		actions = super(MemberAdmin, self).get_actions(request)
		if request.user.groups.filter(name='desk clerk').count():
			if 'register' in actions:
				del actions['register']
		return actions
	
	"""def get_form(self, request, obj=None, **kwargs):
		self.exclude = []	
		if not request.user.groups.filter(name='desk clerk').count() and not request.user.is_superuser:
			self.exclude.append('photo')
		elif request.user.groups.filter(name='desk clerk').count():
			self.fields = ('photo','member_id','university_id','first_name','father_name','grand_father_name','subcity','wereda','house_number','house_phone_number',
			'office_phone_number','cell_phone_number','POBox','birth_date','sex','faculty','campus','department','salary','savings_percentage',
			'employment_type','email','application_date','registration_date','is_registered')
		return super(MemberAdmin, self).get_form(request, obj, **kwargs)"""
	
	def get_readonly_fields(self, request, obj = None):
		if request.user.groups.filter(name='desk clerk').count():
			return ('member_id','is_registered','registration_date') + self.readonly_fields
		if request.user.groups.filter(name='chair').count():
			return ('display_big_photo','photo','member_id','university_id','first_name','father_name','grand_father_name','subcity','wereda','house_number','house_phone_number',
			'office_phone_number','cell_phone_number','POBox','birth_date','sex','faculty','campus','department','salary','savings_percentage',
			'employment_type','email','application_date','registration_date','is_registered') + self.readonly_fields
		return self.readonly_fields
	
	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			obj.save()
		if request.user.groups.filter(name='desk clerk').count():			
			if obj.savings_percentage >= 5:
				if not obj.id:
					try:				
						last_member = Member.objects.all().order_by('-id')[0]
						obj.member_id = "mem-"+str(last_member.id + 1)
					except:
						obj.member_id = "mem-1"
				obj.save()
			else:
				messages.error(request,"The member's savings percentage cannot be less than 5%")
	
	def delete_model(self,request,obj):
		if request.user.groups.filter(name='desk clerk').count():
			if not Savings_Account.objects.filter(member=obj).exists():
				try:
					Savings_Account.objects.get(member=obj).delete()
				except ObjectDoesNotExist:
					messages.warning(request,"The member account does not exists")
				obj.delete()
			else:
				messages.error(request,"Oh Snap! But the member is activated")
		elif request.user.groups.filter(name='chair').count():
			try:
				Savings_Account.objects.get(member=obj).delete()
			except ObjectDoesNotExist:
				messages.warning(request,"The member account does not exists")
			obj.delete()

class LastTransaction(SimpleListFilter):
	title = _('Last deposit date')

    # Parameter for the filter that will be used in the URL query.
	parameter_name = 'last_deposit'

	def lookups(self, request, model_admin):
		return (
            ('zero', _('this month')),
            ('one', _('last month')),
            ('two', _('two months ago')),
            ('three', _('three months ago')),
            ('four', _('four months ago')),
            ('five', _('five months ago')),
            ('six', _('six months ago')),
            ('never', _('never')),
        )

	def queryset(self, request, queryset):

		if self.value() == 'zero':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 1),
                                    last_deposit__lte=date.today())
		elif self.value() == 'one':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 2),
                                    last_deposit__lte=date.today() + relativedelta(months =- 1))
		elif self.value() == 'two':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 3),
                                    last_deposit__lte=date.today() + relativedelta(months =- 2))
		elif self.value() == 'three':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 4),
                                    last_deposit__lte=date.today() + relativedelta(months =- 3))
		elif self.value() == 'four':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 5),
                                    last_deposit__lte=date.today() + relativedelta(months =- 4))
		elif self.value() == 'five':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 6),
                                    last_deposit__lte=date.today() + relativedelta(months =- 5))
		elif self.value() == 'six':
			return queryset.filter(last_deposit__gt=date.today() + relativedelta(months =- 7),
                                    last_deposit__lte=date.today() + relativedelta(months =- 6))
		elif self.value() == 'never':
			return queryset.filter(last_deposit=date(1970, 1, 1))

class AccountTransactionAdmin(admin.ModelAdmin):
	list_display = ['account','action','date','paid_amount','total']
	list_filter = ['date','action']
	search_fields = ['account__member__first_name','account__member__father_name','account__member__grand_father_name']
	ordering = ['date']

class AccountTransactionInline(admin.TabularInline):
	model = Account_Transaction
	extra = 0
	readonly_fields = ('account','date','total',)
	can_delete = False
	def get_readonly_fields(self,request,obj=None):
		if not request.user.groups.filter(name="cashier") and not request.user.is_superuser:
			return ('paid_amount','action',) + self.readonly_fields
		return self.readonly_fields

class SavingsAccountModel(admin.ModelAdmin):
	search_fields = ['member__first_name','member__father_name','member__grand_father_name','account_id']
	list_filter = (LastTransaction,'creation_date','is_active')
	list_display = ['account_id','member','creation_date','deposit','interest','balance','guaranteed','last_deposit_date','is_active']
	ordering = ['is_active','member','creation_date']
	list_per_page = 25
	inlines = [AccountTransactionInline,]
	
	def activate(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name='desk clerk').count():
			rows_updated = queryset.filter(is_active=False).update(is_active=True)
		if rows_updated == 1:
			message_bit = "1 savings account was"
		else:
			message_bit = "%s savings accounts were" % rows_updated
		self.message_user(request, "%s successfully marked as activated." % message_bit)
	activate.short_description = "Mark selected accounts to activate"
	
	def deposit(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name='desk clerk').count():
			for account in queryset:				
				delta = date.today() - account.last_deposit
				if delta.days > 30 and account.is_active:
					monthly = account.savings_percentage * account.member.salary / 100
					interest_rate = Constant.objects.get(id=1).savings_interest_rate
					interest = interest_rate / 1200 * monthly
					total_deposit = account.deposit + monthly
					total_interest = account.interest + interest
					total_amount = total_deposit + total_interest
					rows_updated += queryset.filter(member=account.member).update(deposit=total_deposit,interest=total_interest,balance=total_amount,last_deposit=date.today())		
					Account_Transaction(account=account,action="deposited",date=date.today(),paid_amount=monthly,total=total_amount).save()
				else:
					messages.error(request, "%s's account has already been deposited for %s" % (account.member,datetime.today().strftime("%B")))
		if rows_updated == 1:
			message_bit = "1 savings account was"
		else:
			message_bit = "%s savings account were" % rows_updated
		self.message_user(request, "%s successfully marked as deposited." % message_bit)
	deposit.short_description = "Mark selected accounts to deposit"
	
	def cancel_deposit(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name='desk clerk').count():
			for account in queryset:
				delta = date.today() - account.last_deposit
				if delta.days < 30:
					monthly = account.savings_percentage * account.member.salary / 100
					interest_rate = Constant.objects.get(id=1).savings_interest_rate
					interest = interest_rate / 1200 * monthly
					total_deposit = account.deposit - monthly
					total_interest = account.interest - interest
					total_amount = total_deposit + total_interest
					rows_updated += queryset.filter(member=account.member).update(deposit=total_deposit,interest=total_interest,balance=total_amount,last_deposit=date.today() + relativedelta(months=-1))		
					Account_Transaction.objects.filter(account=account,paid_amount=monthly,date__gt=date.today() + relativedelta(months =- 1),date__lte=date.today()).delete()
				else:
					messages.error(request, "Too late to cancel %s's deposit for %s" % (account.member,account.last_deposit.strftime("%B")))
		if rows_updated == 1:
			message_bit = "1 savings account was"
			self.message_user(request, "%s successfully marked as repaid." % message_bit)
		else:
			message_bit = "%s savings accounts were" % rows_updated
			self.message_user(request, "%s successfully marked for cacellation of last deposit." % message_bit)
	cancel_deposit.short_description = "Mark selected accounts to cancel deposit"
	actions = [deposit,cancel_deposit,activate]

class GuaranteeAdmin(admin.ModelAdmin):
	list_display = ['loan_request','guarantor','amount','get_percent','created_date','is_applied']
	#list_editable = ['created_date']
	list_filter = ['created_date','amount']
	#list_per_page = 2
	search_fields = ['guarantor__first_name','guarantor__father_name','guarantor__grand_father_name']
	ordering = ['created_date']

class GuaranteeInline(admin.TabularInline):
	model = Guarantee
	extra = 1
	exclude = ('applied_amount','percentage','is_applied','is_seen','seen_date')

class LoanRequestAdmin(admin.ModelAdmin):
	
	list_display = ['member','principal','interest', 'amount','request_date','is_guaranteed','accountant_approval','cp_vcp_approval','cashier_grant','is_accepted','is_terminated']
	list_display_links = ['member']
	#list_editable = ['request_date']
	list_filter = ['request_date','is_guaranteed','accountant_approval','cp_vcp_approval','cashier_grant','is_accepted','is_terminated']
	#list_per_page = 2
	search_fields = ['member__first_name','member__father_name','member__grand_father_name']
	ordering = ['request_date']
	#fields = ('member','amount','request_reason','request_date')
	inlines = [GuaranteeInline,]

	def grant(self, request, queryset):
		rows_updated = 0
		if request.user.groups.filter(name='accountant').count():
			rows_updated = queryset.filter(is_guaranteed=True,accountant_approval=False).update(accountant_approval=True)
		elif request.user.groups.filter(name='cashier').count():
			for lr in queryset:
				if lr.cp_vcp_approval:
					constant = Constant.objects.get(id=1)
					interest_rate = constant.loan_interest_rate
					repayment_rate = lr.member.salary / 3 if lr.amount > lr.member.salary / 3 else lr.amount
					amount = lr.amount
					interest = lr.interest
					repayment_date = calculate_repayment_date(amount,repayment_rate)
					try:
						if not Loan_Disbursement.objects.filter(loan_request=lr).exists():
							ld = Loan_Disbursement(loan_request=lr,member=lr.member,principal=lr.principal,interest=interest,amount=amount,remaining=amount,interest_rate=interest_rate,disbursement_date=date.today(),repayment_rate=repayment_rate,repayment_date=repayment_date,last_payment_date=date(1970,1,1))
							ld.save()
							rows_updated += queryset.filter(member=lr.member,cp_vcp_approval=True,cashier_grant=False).update(cashier_grant=True)
					except ObjectDoesNotExist:
						ld = Loan_Disbursement(loan_request=lr,member=lr.member,principal=lr.principal,interst=interest,amount=amount,remaining=amount,interest_rate=interest_rate,disbursement_date=date.today(),repayment_rate=repayment_rate,repayment_date=repayment_date,last_payment_date=date(1970,1,1))
						ld.save()
						rows_updated += queryset.filter(member=lr.member,cp_vcp_approval=True,cashier_grant=False).update(cashier_grant=True)
						
		elif request.user.groups.filter(name='chair').count():
			rows_updated = queryset.filter(accountant_approval=True,cp_vcp_approval=False).update(cp_vcp_approval=True)
				
		if rows_updated == 1:
			message_bit = "1 loan request was"
			self.message_user(request, "%s successfully marked as accepted." % message_bit)
		else:
			message_bit = "%s loan requests were" % rows_updated
			self.message_user(request, "%s successfully marked as accepted." % message_bit)
	grant.short_description = "Mark selected loan requests as approved/disbursed"

	def revoke(self, request, queryset):
		rows_updated = 0
		if request.user.groups.filter(name='accountant').count():
			queryset.update(cashier_grant=False)
			for lr in queryset:
				if not lr.cashier_grant:
					try:
						ld = Loan_Disbursement.objects.get(loan_request=lr)
						ld.delete()
						rows_updated += queryset.filter(member=lr.member,is_terminated=False).update(cashier_grant=False,cp_vcp_approval=False,accountant_approval=False)
					except ObjectDoesNotExist:
						messages.error(request,"Oh snap!, %s's loan disbursement was already deleted" %lr.member)
						rows_updated += queryset.filter(member=lr.member,is_terminated=False).update(cashier_grant=False,cp_vcp_approval=False,accountant_approval=False)
		if request.user.groups.filter(name='cashier').count():
			for lr in queryset:
				if not lr.is_accepted:
					try:
						ld = Loan_Disbursement.objects.get(loan_request=lr)
						ld.delete()
						rows_updated += queryset.filter(member=lr.member,is_terminated=False).update(cashier_grant=False)
					except ObjectDoesNotExist:
						messages.error(request,"Oh snap!, %s's loan disbursement was already deleted" %lr.member)
						rows_updated += queryset.filter(member=lr.member).update(cashier_grant=False)
		if request.user.groups.filter(name='chair').count():
			for lr in queryset:
				if not lr.cashier_grant:
					try:
						ld = Loan_Disbursement.objects.get(loan_request=lr)
						ld.delete()
						rows_updated += queryset.filter(member=lr.member,is_terminated=False).update(cashier_grant=False,cp_vcp_approval=False)
					except ObjectDoesNotExist:
						messages.error(request,"Oh snap!, %s's loan disbursement was already deleted" %lr.member)
						rows_updated += queryset.filter(member=lr.member,is_terminated=False).update(cashier_grant=False,cp_vcp_approval=False)

		if rows_updated == 1:
			message_bit = "1 loan request was"
			self.message_user(request, "%s successfully marked as rejected." % message_bit)
		else:
			message_bit = "%s loan requests were" % rows_updated
			self.message_user(request, "%s successfully marked as rejected." % message_bit)
		
	revoke.short_description = "Mark selected loan requests as cancelled"
	
	def apply_guarantee(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name="desk clerk").count():
			for lr in queryset:
				if not lr.is_guaranteed:
					try:
						guarantees = Guarantee.objects.filter(loan_request=lr)
						for g in guarantees:								
							if not g.is_applied and not lr.is_guaranteed:
								guaranteed = lr.guaranteed + g.amount
								is_guaranteed = True if lr.guaranteed >= lr.required_guarantee_amount else False
								g.is_applied =True
								rows_updated += queryset.filter(id=lr.id).update(guaranteed=guaranteed,is_guaranteed=is_guaranteed)
								g.save()
							elif lr.is_applied:
								g.delete()
					except ObjectDoesNotExist:
						pass
				else:
					Guarantee.objects.filter(loan_request=lr,is_applied=False).delete()
					messages.warning(request,"%s's loan request has already been guaranteed" %lr.member)
		if rows_updated == 1:
			message_bit = "1 loan request was"
		else:
			message_bit = "%s loan requests were" % rows_updated
		self.message_user(request, "%s successfully marked as updated." % message_bit)
	apply_guarantee.short_description = "Mark selected loan requests to apply guarantee"
			
	actions = [grant,revoke,apply_guarantee]
	
	def get_actions(self, request):
		actions = super(LoanRequestAdmin, self).get_actions(request)
		if request.user.groups.filter(name='desk clerk').count():
			if 'delete_selected' in actions:
				del actions['delete_selected']
			if 'accept' in actions:
				del actions['grant']
			if 'reject' in actions:
				del actions['revoke']
		if request.user.groups.filter(name='accountant').count() or request.user.groups.filter(name='cashier').count():
			if 'delete_selected' in actions:
				del actions['delete_selected']
		return actions
	
	def get_form(self, request, obj=None, **kwargs):
		self.exclude = []	
		if not request.user.groups.filter(name='chair').count() and not request.user.is_superuser:
			self.exclude.append('is_seen')
			self.exclude.append('is_accepted')
			self.exclude.append('is_terminated')
			self.exclude.append('seen_date')
		return super(LoanRequestAdmin, self).get_form(request, obj, **kwargs)
	
	def get_readonly_fields(self, request, obj = None):
		if request.user.groups.filter(name='cashier').count():
			return ('member','amount','current_amount','principal','interest','required_guarantee_amount','guaranteed','request_date','request_reason','is_guaranteed','accountant_approval','cp_vcp_approval','comments','cashier_grant','required_adjustment') + self.readonly_fields
		if request.user.groups.filter(name='accountant').count():
			return ('member','amount','current_amount','principal','interest','required_guarantee_amount','guaranteed','request_date','request_reason','is_guaranteed','cashier_grant','cp_vcp_approval','accountant_approval','required_adjustment') + self.readonly_fields
		if request.user.groups.filter(name='chair').count():
			return ('member','amount','current_amount','principal','interest','guaranteed','request_date','request_reason','is_guaranteed','cashier_grant','accountant_approval','comments','cp_vcp_approval','is_accepted','is_seen','is_terminated','seen_date','required_adjustment') + self.readonly_fields
		if request.user.groups.filter(name='desk clerk').count():
			return ('amount','current_amount','interest','required_guarantee_amount','guaranteed','is_guaranteed','accountant_approval','cashier_grant','cp_vcp_approval','seen_date','is_seen','comments','is_accepted','is_terminated','required_adjustment') + self.readonly_fields
		return self.readonly_fields

	def save_model(self, request, obj, form, change):
		if request.user.is_superuser:
			obj.save()
		if request.user.groups.filter(name='desk clerk').count():
			if Loan_Request.objects.filter(member=obj.member,cashier_grant=True,is_terminated=False).exists():
				messages.error(request,"Oh snap! %s has already recieved a loan" %obj.member)
			else:
				delta = date.today() - obj.member.registration_date
				if delta.days > 120:
					repayment_rate = obj.member.salary / 3
					interest_rate = Constant.objects.get(id=1).loan_interest_rate
					obj.amount,obj.interest = calcualte_total_loan_amount(obj.principal,interest_rate, repayment_rate)
					repayment_rate = repayment_rate if repayment_rate < obj.amount else obj.amount
					repayment_date = calculate_repayment_date(obj.amount,repayment_rate)
					period = repayment_date - date.today()
					balance = Savings_Account.objects.get(member=obj.member).balance
					if balance > 120000:
						loan_limit = balance
					else:
						loan_limit = 120000 if 8 * balance > 120000 else 8 * balance
					if obj.amount <= loan_limit:
						Loan_Request.objects.filter(member=obj.member,cashier_grant=False).delete()
						obj.required_guarantee_amount = obj.amount - balance if obj.amount > balance else 0
						guaranteed_amount = balance if balance <= obj.amount else obj.amount
						Savings_Account.objects.filter(member=obj.member).update(guaranteed=guaranteed_amount)
						if obj.id and obj.amount != obj.current_amount:
							Guarantee.objects.filter(loan_request=obj).delete()
							obj.guaranteed = 0
							obj.is_guaranteed = False
						else:
							obj.is_guaranteed = True if obj.guaranteed >= obj.required_guarantee_amount else False					
						obj.current_amount = obj.amount					
						obj.save()		
					elif obj.amount > loan_limit:
						messages.error(request,"Oh snap! %s's loan can't exceed %d birr" %(obj.member,loan_limit))
					elif period.days > 2880:
						messages.error(request,"Oh snap! %s's loan can't be repayed within 8 years" % obj.member)					
				else:
					messages.error(request,"Cannot make a loan request before %s" %obj.registration_date + relativedelta(months=+4))

class LoanRenewalAdmin(admin.ModelAdmin):
	list_display = ['loan','renewal_date','previous_loan_amount','previous_repayment_date','current_loan_amount','current_repayment_date']
	list_filter = ['current_repayment_date','previous_repayment_date']
	search_fields = ['loan__member__first_name','loan__member__father_name','loan__member__grand_father_name']
	ordering = ['renewal_date']

class RenewalInline(admin.TabularInline):
	model = Loan_Renewal
	extra = 1
	max_num = 1
	exclude = ('member','is_seen','seen_date')
	readonly_fields = ('loan','renewal_date','previous_repayment_date','previous_loan_amount','current_repayment_date','current_loan_amount')
	can_delete = False

class LoanExtensionAdmin(admin.ModelAdmin):
	list_display = ['loan','extension_date','previous_repayment_date','current_repayment_date']
	list_filter = ['current_repayment_date','previous_repayment_date']
	search_fields = ['loan__member__first_name','loan__member__father_name','loan__member__grand_father_name']
	ordering = ['extension_date']

class ExtensionInline(admin.TabularInline):
	model = Loan_Extension
	extra = 1
	max_num = 1
	exclude = ('member','is_seen','seen_date')
	readonly_fields = ('loan','extension_date','previous_repayment_date','current_repayment_date')
	can_delete = False

class LoanTransactionAdmin(admin.ModelAdmin):
	list_display = ['loan','action','date','paid_amount','total']
	list_filter = ['date','action']
	search_fields = ['loan__member__first_name','loan__member__father_name','loan__member__grand_father_name']
	ordering = ['date']

class LoanTransactionInline(admin.TabularInline):
	model = Loan_Transaction
	extra = 0
	readonly_fields = ('loan','date','total','extended_from','extended_to','renewed_from','renewed_to','payment_type','is_settled')
	#can_delete = False
	def get_readonly_fields(self,request,obj=None):
		if not request.user.groups.filter(name="desk clerk") and not request.user.is_superuser:
			return ('paid_amount','action',) + self.readonly_fields
		return self.readonly_fields
	
class LoanDisbursementAdmin(admin.ModelAdmin):
	list_display = ['member','disbursement_date','principal','interest','amount','repayment_date','remaining','repayment_rate','last_payment_on','last_payment_amount','is_activated','is_settled']
	list_display_links = []
	#list_editable = ['request_date']
	list_filter = ['disbursement_date','repayment_date','is_activated']
	#list_per_page = 2
	search_fields = ['member__first_name','member__father_name','member__grand_father_name']
	ordering = ['disbursement_date']
	#fields = ('member','amount','request_reason','request_date')
	inlines = [LoanTransactionInline,RenewalInline,ExtensionInline,]	
	
	#def __init__(self, *args, **kwargs):
		#super(LoanDisbursementAdmin, self).__init__(*args, **kwargs)
		#self.list_display_links = (None, )

	def get_readonly_fields(self, request, obj = None):
		if request.user.groups.filter(name='desk clerk').count():
			return ('member','principal','interest','amount','last_payment_amount','guaranteed','is_guaranteed','remaining','interest_rate','disbursement_date','repayment_date',
					'is_renewed','is_extended','is_settled','is_seen','seen_date','is_activated','repayment_rate','settlement_date','last_payment_date','loan_request') + self.readonly_fields
		return self.readonly_fields
	
	def get_actions(self, request):
		actions = super(LoanDisbursementAdmin, self).get_actions(request)
		if request.user.groups.filter(name='desk clerk').count():
			if 'delete_selected' in actions:
				del actions['delete_selected']
		return actions
	
	def repay(self, request, queryset):
		rows_updated = 0
		if request.user.groups.filter(name='desk clerk').count():
			for ld in queryset:
				if ld.is_activated:
					delta = date.today() - ld.last_payment_date
					if delta.days > 30:
						repayment_rate = ld.repayment_rate if ld.repayment_rate < ld.remaining else ld.remaining
						value = ld.remaining - ld.repayment_rate
						total_paid = ld.amount - value
						paid = ld.repayment_rate
						if not value:
							rows_updated += queryset.filter(member=ld.member,is_settled=False).update(remaining=value,repayment_rate=repayment_rate,last_payment_amount=paid,last_payment_date=date.today(),settlement_date=date.today(),is_settled=True)
							Loan_Transaction(loan=ld,action='repaid',date=date.today(),paid_amount=paid,total=total_paid,payment_type="procedural").save()
							try:
								lr = Loan_Request.objects.get(id = ld.loan_request.id)
								lr.is_terminated = True
								lr.save()
							except ObjectDoesNotExist:
								messages.error(request,"Oh Snap! %s's loan request had already been deleted" % ld.member)
						else:
							rows_updated += queryset.filter(member=ld.member,is_settled=False).update(remaining=value,repayment_rate=repayment_rate,last_payment_amount=paid,last_payment_date=date.today())		
							Loan_Transaction(loan=ld,action='repaid',date=date.today(),paid_amount=paid,total=total_paid,payment_type="procedural").save()
					else:
						messages.error(request, "%s's loan repayment has already been made for %s" % (ld.member,datetime.today().strftime("%B")))
		if rows_updated == 1:
			message_bit = "1 loan disbursement was"
			self.message_user(request, "%s successfully marked as repaid." % message_bit)
		else:
			message_bit = "%s loan disbursements were" % rows_updated
			self.message_user(request, "%s successfully marked as repaid." % message_bit)
	repay.short_description = "Mark selected loan disbursements as repaid"
	
	def cancel_repayment(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name='desk clerk').count():
			for ld in queryset:
				delta = date.today() - ld.last_payment_date
				if delta.days < 30:
					value = ld.remaining + ld.last_payment_amount
					rows_updated += queryset.filter(member=ld.member,is_settled=False).update(remaining=value,last_payment_date=date.today() + relativedelta(months=-1))		
					Loan_Transaction.objects.filter(loan=ld,paid_amount=ld.last_payment_amount,date__gt=date.today() + relativedelta(months =- 1),date__lte=date.today()).delete()
				else:
					messages.error(request, "Oh Snap! Too late to cancel %s's last payment for %s" % (ld.member,ld.last_payment_date.strftime("%B")))
		if rows_updated == 1:
			message_bit = "1 loan disbursement was"
			self.message_user(request, "%s successfully marked as repaid." % message_bit)
		else:
			message_bit = "%s loan disbursements were" % rows_updated
			self.message_user(request, "%s successfully marked for cacellation of last repayment." % message_bit)
	cancel_repayment.short_description = "Mark selected loan disbursements to cancel last repayment"

	def activate(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name='desk clerk').count():
			for ld in queryset:
				try:
					lr = Loan_Request.objects.get(id=ld.loan_request.id)
					lr.is_accepted = True
					lr.save()
					rows_updated += queryset.filter(loan_request=lr,is_activated=False).update(is_activated=True)
				except ObjectDoesNotExist:
					messages.error(request,"Oh snap! the corresponding loan request has been deleted")
					rows_updated += queryset.filter(loan_request=ld.loan_request,is_activated=False).update(is_activated=True)
		if rows_updated == 1:
			message_bit = "1 loan request was"
			self.message_user(request, "%s successfully marked as activated." % message_bit)
		else:
			message_bit = "%s loan requests were" % rows_updated
			self.message_user(request, "%s successfully marked as activated." % message_bit)
		
	activate.short_description = "Mark seleced loan disbursements as activated"
	
	def deactivate(self,request,queryset):
		rows_updated=0
		if request.user.groups.filter(name='desk clerk').count():
			for ld in queryset:
				if ld.is_activated and ld.last_payment_on() == "Pending":
					try:
						lr = Loan_Request.objects.get(id=ld.loan_request.id)
						lr.is_accepted = False
						lr.save()
						rows_updated += queryset.filter(loan_request=lr,is_activated=True).update(is_activated=False)
					except ObjectDoesNotExist:
						messages.error(request,"Oh snap! %s's loan request has already been deleted" % ld.member)
						rows_updated += queryset.filter(loan_request=ld.loan_request,is_activated=True).update(is_activated=False)
				elif ld.last_payment_date != date(1970,1,1):
					messages.error(request,"Oh snap! %s's loan disbursement has already started repayment" % ld.member)
		if rows_updated == 1:
			message_bit = "1 loan request was"
			self.message_user(request, "%s successfully marked as deactivated." % message_bit)
		else:
			message_bit = "%s loan requests were" % rows_updated
			self.message_user(request, "%s successfully marked as deactivated." % message_bit)
		
	deactivate.short_description = "Mark seleced loan disbursements as deactivated"
					
	actions = [repay,cancel_repayment,activate,deactivate]
	
class ConstantsAdmin(admin.ModelAdmin):
	list_display = ['savings_interest_rate','loan_interest_rate']

class DividendAdmin(admin.ModelAdmin):
	list_display = ['amount','creation_date','total_savings','is_applied']
	list_filter = ['creation_date','is_applied']
	
	def get_readonly_fields(self, request, obj = None):
		if request.user.groups.filter(name="chair").count():
			return ('total_savings','is_applied',) + self.readonly_fields
		elif request.user.groups.filter(name="cashier").count():
			return ('amount','creation_date','total_savings','is_applied',) + self.readonly_fields
		return self.readonly_fields
	
	def apply_dividend(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name="cashier").count():			
			for nd in queryset:
				if not nd.is_applied:
					for member in Member.objects.filter(is_registered=True):
						if Dividends_Account.objects.filter(member=member).exists():
							balance = Savings_Account.objects.get(member=member).balance if Savings_Account.objects.filter(member=member).exists() else 0
							Dividends_Account.objects.filter(member=member).update(last_amount= F('last_amount') + (balance / nd.total_savings) * nd.amount,amount = F('amount') + (balance / nd.total_savings) * nd.amount,is_withdrawn=False)
						else:
							balance = Savings_Account.objects.get(member=member).balance if Savings_Account.objects.filter(member=member).exists() else 0
							amount = (balance / nd.total_savings) * nd.amount
							Dividends_Account(member=member,amount=amount,last_amount=amount,creation_date=date.today(),is_withdrawn=False).save()
					rows_updated += queryset.filter(is_applied=False).update(is_applied=True)
		if rows_updated == 1:
			message_bit = "1 dividend was"
		else:
			message_bit = "%s dividends were" % rows_updated
		self.message_user(request, "%s successfully marked as applied." % message_bit)
	
	apply_dividend.short_description = "Mark the following dividends as applied"
	actions = [apply_dividend]

class DividendsAccountAdmin(admin.ModelAdmin):
	list_display = ['dividend_id','member','creation_date','amount','withdrawn','last_amount','last_withdrawal_date','is_withdrawn']
	list_filter = ['creation_date','is_withdrawn']
	search_fields = ['member__first_name','member__father_name','member__grand_father_name','dividend_id']
	ordering = ['creation_date']
	
	def withdraw(self,request,queryset):
		rows_updated = 0
		if request.user.groups.filter(name="cashier").count():
			rows_updated = queryset.filter(last_amount__gt=0,is_withdrawn=False).update(withdrawn=F('withdrawn') + F('last_amount'),is_withdrawn=True,last_amount=0,last_withdrawal=date.today())
		
		if rows_updated == 1:
			message_bit = "1 dividend was"
		else:
			message_bit = "%s dividends were" % rows_updated
		self.message_user(request, "%s successfully marked as applied." % message_bit)	
	withdraw.short_description = "Mark the following dividends as withdrawn"
	actions=[withdraw]

class NotificationAdmin(admin.ModelAdmin):
	list_display = ['notification_id','to','message','sent_date']
	list_filter = ['sent_date']
	search_fields = ['to__first_name','to__father_name','to__grand_father_name','notification_id']
	ordering = ['sent_date']
	
	def get_readonly_fields(self,request, obj = None):
		if not request.user.is_superuser:
			return ('notification_id',) + self.readonly_fields
		return self.readonly_fields


admin.site.register(Member,MemberAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Savings_Account,SavingsAccountModel)
admin.site.register(Dividends_Account,DividendsAccountAdmin)
admin.site.register(Dividend,DividendAdmin)
admin.site.register(Loan_Request,LoanRequestAdmin)
admin.site.register(Loan_Disbursement,LoanDisbursementAdmin)
admin.site.register(Loan_Renewal,LoanRenewalAdmin)
admin.site.register(Loan_Extension,LoanExtensionAdmin)
admin.site.register(Guarantee,GuaranteeAdmin)
admin.site.register(Constant,ConstantsAdmin)
admin.site.register(Loan_Transaction,LoanTransactionAdmin)
admin.site.register(Account_Transaction)
