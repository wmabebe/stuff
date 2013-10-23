from django.db import models
from members.models import Member
from balance_and_dividend.models import Savings_Account 
from datetime import *
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ObjectDoesNotExist
from constants.models import *
from loan import *

# Create your models here.
		
class Loan_Request(models.Model):
	member = models.ForeignKey(Member,limit_choices_to={'registration_date__lt':date.today() + relativedelta(months=-4)})
	principal = models.DecimalField(max_digits=20,decimal_places=2)
	interest = models.DecimalField(max_digits=20,decimal_places=2)
	amount = models.DecimalField(max_digits=20,decimal_places=2,verbose_name="Total Amount")
	current_amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	required_guarantee_amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	guaranteed = models.DecimalField(max_digits=20,decimal_places=2,default=0)	
	request_reason = models.TextField()
	request_date = models.DateField()
	accountant_approval = models.BooleanField()
	cp_vcp_approval = models.BooleanField()
	cashier_grant = models.BooleanField()
	is_guaranteed = models.BooleanField(verbose_name="Guaranteed")
	is_accepted = models.BooleanField(verbose_name="Accepted")
	is_terminated = models.BooleanField(verbose_name="Terminated")
	required_adjustment = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	is_seen = models.BooleanField()
	seen_date = models.DateField(default=None,null=True,blank=True)
	comments = models.TextField(default=None,null=True,blank=True)
	def __unicode__(self):
		return u'%s %d Birr' % (self.member.first_name+" "+self.member.father_name+" "+self.member.grand_father_name,self.principal)

class Loan_Disbursement(models.Model):
	member = models.ForeignKey(Member)
	loan_request = models.ForeignKey(Loan_Request)
	principal = models.DecimalField(max_digits=20,decimal_places=2)
	interest = models.DecimalField(max_digits=20,decimal_places=2)
	amount = models.DecimalField(max_digits=20,decimal_places=2,verbose_name="Total Amount")
	guaranteed = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	remaining = models.DecimalField(max_digits=20,decimal_places=2,default=0,verbose_name="Outstanding Balance")
	interest_rate = models.DecimalField(max_digits=4,decimal_places=2)
	disbursement_date = models.DateField()
	last_payment_date = models.DateField(default=date(1970,1,1))
	last_payment_amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	repayment_rate = models.DecimalField(max_digits=20,decimal_places=2,verbose_name="Monthly payment")
	repayment_date = models.DateField(verbose_name="Expected settlement date")
	settlement_date = models.DateField(default=None,null=True,blank=True)
	is_guaranteed = models.BooleanField()
	is_activated = models.BooleanField(verbose_name="Activated")
	is_renewed = models.BooleanField(verbose_name="Renewed")
	is_extended = models.BooleanField(verbose_name="Extended")
	is_settled = models.BooleanField(verbose_name="Settled")
	is_seen = models.BooleanField()
	seen_date = models.DateField(default=None,null=True,blank=True)
	def last_payment_on(self):
		if self.last_payment_date == date(1970,1,1) or self.remaining == self.amount:
			return "Pending"
		return self.last_payment_date
	def __unicode__(self):
		return u'%s     %d Birr' % (self.member.first_name+" "+self.member.father_name+" "+self.member.grand_father_name,self.principal)
class Guarantee(models.Model):
	loan_request = models.ForeignKey(Loan_Request)
	guarantor = models.ForeignKey(Member, null=True, related_name="guarantor",limit_choices_to={'is_registered':True,'employment_type':"Permanent"})
	percentage = models.DecimalField(max_digits=5,decimal_places=2,default=0)
	amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	applied_amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	is_applied = models.BooleanField()
	created_date = models.DateField(default=date.today())
	is_seen = models.BooleanField()
	seen_date = models.DateField(default=None,null=True,blank=True)
	def get_percent(self):
		return str(self.percentage) + "%"
	get_percent.short_description = "Percentage"
	def __unicode__(self):
		return u'%s'%(self.guarantor.first_name)
	
	def save(self, *args, **kwargs):
		if self.loan_request.member != self.guarantor and not self.loan_request.accountant_approval:
			remaining = Savings_Account.objects.get(member=self.guarantor).balance - Savings_Account.objects.get(member=self.guarantor).guaranteed
			if self.amount <= remaining:
				try:				
					if self.amount == 0 and self.id:
						super(Guarantee, self).delete(*args, **kwargs)			
					elif self.amount > 0:
						lr = Loan_Request.objects.get(id=self.loan_request.id,cashier_grant=False)			
						if self.amount >= lr.required_guarantee_amount:
							Guarantee.objects.filter(loan_request=self.loan_request,is_applied=True).exclude(id=self.id).delete()
							lr.guaranteed = lr.required_guarantee_amount
							lr.is_guaranteed = True
							lr.save()
							self.applied_amount = lr.required_guarantee_amount
							self.amount = self.applied_amount
							self.is_applied = True
							self.percentage = self.amount * 100 / lr.required_guarantee_amount
							super(Guarantee, self).save(*args, **kwargs)
							Savings_Account.objects.filter(member=self.guarantor).update(guaranteed=self.amount)
						elif lr.is_guaranteed:
							if self.id and self.is_applied and self.applied_amount > self.amount:
								difference = self.applied_amount - self.amount
								lr.guaranteed -= difference
								lr.is_guaranteed = False
								lr.accountant_approval = False
								lr.cp_vcp_approval = False
								lr.save()
								self.applied_amount = self.amount
								if self.applied_amount <= 0:
									super(Guarantee, self).delete(*args, **kwargs)
								else:
									self.is_applied = True
									self.percentage = self.amount * 100 / lr.required_guarantee_amount
									super(Guarantee, self).save(*args, **kwargs)
									Savings_Account.objects.filter(member=self.guarantor).update(guaranteed=self.amount)
							elif not self.id and self.is_applied and self.applied_amount < self.amount:
								excess = self.amount - self.applied_amount if self.amount < lr.required_guarantee_amount else lr.required_guarantee_amount - self.applied_amount
								difference = excess
								cascaded = False
								other_guarantees = Guarantee.objects.filter(loan_request=self.loan_request)
								for og in other_guarantees:
									if og.id != self.id and not cascaded:
										if og.applied_amount >= excess:
											og.applied_amount -= excess
											og.amount = og.applied_amount
											og.percentage = og.amount * 100 / lr.required_guarantee_amount 
											if og.applied_amount <= 0:
												og.delete()
											else:
												og.save()								
											cascaded = True
										else:
											excess -= og.applied_amount
											og.applied_amount = 0
											og.amount = 0
											og.delete()
											if excess <= 0:
												cascaded = True
								self.applied_amount += difference
								self.amount = self.applied_amount
								self.is_applied = True
								self.percentage = self.amount * 100 / lr.required_guarantee_amount
								super(Guarantee, self).save(*args, **kwargs)
								Savings_Account.objects.filter(member=self.guarantor).update(guaranteed=self.amount)
						else:
							if self.id and self.is_applied and self.applied_amount > self.amount:
								difference = self.applied_amount - self.amount
								lr.guaranteed -= difference
								lr.save()
								self.applied_amount = self.amount
								if self.applied_amount <= 0:
									super(Guarantee, self).delete(*args, **kwargs)
								else:
									self.is_applied = True
									self.percentage = self.amount * 100 / lr.required_guarantee_amount
									super(Guarantee, self).save(*args, **kwargs)
									Savings_Account.objects.filter(member=self.guarantor).update(guaranteed=self.amount)
							elif self.id and self.is_applied and self.applied_amount < self.amount:
								extra = self.amount - self.applied_amount if self.amount < lr.required_guarantee_amount else lr.required_guarantee_amount - self.applied_amount
								lr.guaranteed += extra
								if lr.guaranteed >= lr.required_guarantee_amount:
									lr.is_guaranteed = True
								lr.save()
								difference = extra
								cascaded = False
								other_guarantees = Guarantee.objects.filter(loan_request=self.loan_request)
								for og in other_guarantees:
									if og.id != self.id and not cascaded:
										if og.applied_amount <= extra:
											og.applied_amount -= extra
											og.amount = og.applied_amount
											og.percentage = og.amount * 100 / lr.required_guarantee_amount
											if og.amount <= 0:
												del(og)
											else:
												og.save()
											cascaded = True
										else:
											extra -= og.applied_amount
											og.applied_amount = 0
											og.amount = 0
											del(og)
											if extra <= 0:
												cascaded = True
								self.applied_amount += difference
								self.amount = self.applied_amount
								self.is_applied = True
								self.percentage = self.amount * 100 / lr.required_guarantee_amount
								super(Guarantee, self).save(*args, **kwargs)
								Savings_Account.objects.filter(member=self.guarantor).update(guaranteed=self.amount)
							elif not self.id:				
								self.amount = self.amount if self.amount + lr.guaranteed < lr.required_guarantee_amount else lr.required_guarantee_amount - lr.guaranteed
								self.applied_amount = self.amount
								lr.guaranteed += self.amount
								lr.is_guaranteed = True if lr.guaranteed >= lr.required_guarantee_amount else False
								lr.save()
								self.is_applied = True if self.amount > 0 else False
								if self.is_applied:
									self.percentage = self.amount * 100 / lr.required_guarantee_amount
									super(Guarantee, self).save(*args, **kwargs)
									Savings_Account.objects.filter(member=self.guarantor).update(guaranteed=self.amount)
				except ObjectDoesNotExist:
					pass
	def delete(self, *args, **kwargs):
		if self.is_applied and self.amount > 0:
			try:
				lr = Loan_Request.objects.get(id=self.loan_request.id,cashier_grant=False)
				lr.guaranteed -= self.amount
				lr.save()
				if lr.is_guaranteed < lr.required_guarantee_amount:
					lr.cp_vcp_approval = False
					lr.accountant_approval = False
					lr.is_guaranteed = False					
				lr.save()
				super(Guarantee, self).delete(*args, **kwargs)
			except ObjectDoesNotExist:
				super(Guarantee, self).delete(*args, **kwargs)
		else:
			super(Guarantee, self).delete(*args, **kwargs)
		
class Loan_Renewal(models.Model):
	loan = models.ForeignKey(Loan_Disbursement)
	previous_loan_amount = models.DecimalField(max_digits=20,decimal_places=2)
	current_loan_amount = models.DecimalField(max_digits=20,decimal_places=2)
	previous_repayment_date = models.DateField()
	current_repayment_date = models.DateField()
	member = models.ForeignKey(Member)
	renewal_amount = models.DecimalField(max_digits=20,decimal_places=2,verbose_name="Increase loan to (amount)")
	renewal_date = models.DateField()
	is_seen = models.BooleanField()
	seen_date = models.DateField(default=None,null=True,blank=True)
	
	def __unicode__(self):
		return u'%s increased by %d Birr' % (self.loan,self.renewal_amount)
	
	def save(self,*args,**kwargs):
		if not self.loan.is_settled and self.renewal_amount > 0:
			ld = self.loan
			interest_rate = Constant.objects.get(id=1).loan_interest_rate
			current_repayment_rate = ld.repayment_rate
			default_repayment_rate = ld.member.salary / 3		
			renewed_principal = self.renewal_amount
			renewed_amount_wcrr,renewed_interest_wcrr = calcualte_total_loan_amount(renewed_principal,interest_rate,current_repayment_rate)  # wcrr: with current repayment rate
			renewed_amount_wdrr,renewed_interest_wdrr = calcualte_total_loan_amount(renewed_principal,interest_rate,default_repayment_rate) #wdrr: with default repayment rate
			if renewed_amount_wcrr + ld.remaining <= ld.amount:
				new_repayment_date = calculate_repayment_date(renewed_amount_wcrr + ld.remaining,current_repayment_rate)
				if new_repayment_date <= ld.disbursement_date + relativedelta(months=+96):
					self.previous_loan_amount = ld.amount
					self.previous_repayment_date = ld.repayment_date
					self.member = ld.member
					self.renewal_date = date.today()
					self.current_repayment_date = new_repayment_date
					self.current_loan_amount = ld.amount + renewed_amount_wcrr
					ld.principal += renewed_principal
					ld.interest += renewed_interest_wcrr
					ld.amount += renewed_amount_wcrr
					ld.remaining += renewed_amount_wcrr
					ld.repayment_date = new_repayment_date
					ld.is_renewed = True
					ld.save()				
					super(Loan_Renewal, self).save(*args, **kwargs)
			elif  renewed_amount_wdrr + ld.remaining <= ld.amount:
				new_repayment_date = calculate_repayment_date(renewed_amount_wdrr + ld.remaining,default_repayment_rate)
				if new_repayment_date <= ld.disbursement_date + relativedelta(months=+96):
					self.previous_loan_amount = ld.amount
					self.previous_repayment_date = ld.repayment_date
					self.member = ld.member
					self.renewal_date = date.today()
					self.current_repayment_date = new_repayment_date
					self.current_loan_amount = ld.amount + renewed_amount_wcrr
					ld.principal += renewed_principal
					ld.interest += renewed_interest_wdrr
					ld.amount += renewed_amount_wdrr
					ld.remaining += renewed_amount_wdrr
					ld.repayment_date = new_repayment_date
					ld.is_renewed = True
					ld.save()
					super(Loan_Renewal, self).save(*args, **kwargs)			
			
class Loan_Extension(models.Model):
	loan = models.ForeignKey(Loan_Disbursement)
	extension_months = models.IntegerField(default=0,verbose_name="Repay remaining loan within (months)")
	member = models.ForeignKey(Member)
	extension_date = models.DateField()
	previous_repayment_date = models.DateField()
	current_repayment_date = models.DateField()
	is_seen = models.BooleanField()
	seen_date = models.DateField(default=None,null=True,blank=True)
	def __unicode__(self):
		return u'%s from %s to %s' % (self.loan,self.previous_repayment_date,self.current_repayment_date)
	
	def save(self, *args, **kwargs):
		ld = self.loan
		if not self.loan.is_settled and self.extension_months > 0 and date.today() + relativedelta(months =+ self.extension_months) <= ld.disbursement_date + relativedelta(months =+ 96):
			self.previous_loan_amount = self.loan.amount
			self.previous_repayment_date = self.loan.repayment_date
			self.member = self.loan.member
			self.extension_date = date.today()
			if ld.last_payment_date.month !=  date.today().month or ld.last_payment_date == date(1970,1,1):
				time = int(self.extension_months) - 1
			else:
				time = int(self.extension_months)
			self.current_repayment_date = date.today() + relativedelta( months =+ time )
			ld.repayment_date = self.current_repayment_date
			ld.repayment_rate = self.loan.remaining / self.extension_months
			ld.is_extended = True
			ld.save()
			super(Loan_Extension, self).save(*args, **kwargs)
