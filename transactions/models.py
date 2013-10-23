from django.db import models
from loan.models import *
from balance_and_dividend.models import *
from members.models import *
from dateutil.relativedelta import relativedelta

# Create your models here.
class Loan_Transaction(models.Model):
	EVENTS = (
	("disbursed","disbursed"),
	("repaid","repaid"),
	("extended","extended"),
	("renewed","renewed"),
	("settled","settled"),
	)

	loan = models.ForeignKey(Loan_Disbursement)
	action = models.CharField(max_length=50,choices=EVENTS,default="repaid")
	date = models.DateField(default=date.today())
	paid_amount = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	total = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	extended_from = models.DateField(default=None,null=True,blank=True)
	extended_to = models.DateField(default=None,null=True,blank=True)
	renewed_from = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	renewed_to = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	payment_type = models.CharField(max_length=50,default="unprocedural")
	is_settled = models.BooleanField(verbose_name="Settled")
	
	def __unicode__(self):
		return u'%s' % (self.loan.member)
	
	def save(self,*args,**kwargs):
		if not self.loan.is_settled and self.paid_amount > 0 and self.action == "repaid":
			ld = self.loan
			self.paid_amount = self.paid_amount if self.paid_amount <= ld.remaining else ld.remaining
			ld.last_payment_amount = self.paid_amount
			ld.remaining -= self.paid_amount
			ld.last_payment_date = date.today()
			self.total += self.paid_amount
			self.date = date.today()
			if ld.remaining >= ld.amount:
				self.is_settled = True
				ld.is_settled = True
			ld.save()
			super(Loan_Transaction, self).save(*args, **kwargs)
	
	def delete(self,*args,**kwargs):
		delta = date.today() - self.loan.last_payment_date
		if not self.loan.is_settled and delta.days < 30 and self.action == "repaid":
			self.loan.remaining += self.paid_amount
			super(Loan_Transaction, self).delete(*args, **kwargs)
			self.loan.last_payment_date = Loan_Transaction.objects.latest('id').date
			self.loan.save()

class Account_Transaction(models.Model):
	EVENTS = (
	("created","created"),
	("deposited","deposited"),
	("withdrwan","withdrwan"),
	("withdrwan","withdrwan"),
	("taken","taken"),
	)
	account = models.ForeignKey(Savings_Account)
	action = models.CharField(max_length=50,choices=EVENTS)
	date = models.DateField(default=date.today())
	paid_amount = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	total = models.DecimalField(default=0,max_digits=20,decimal_places=2)
	
	def __unicode__(self):
		return u'%s' % (self.account.member)
	
