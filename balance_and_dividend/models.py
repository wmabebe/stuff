from django.db import models

# Create your models here.
from django.db import models
from members.models import Member
from datetime import *

# Create your models here.
class Savings_Account(models.Model):
	account_id = models.CharField(max_length=20)
	member = models.ForeignKey(Member)
	deposit = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	interest = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	balance = models.DecimalField(max_digits=20,decimal_places=2,default=0,verbose_name="Total Balance")
	guaranteed = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	savings_percentage = models.IntegerField(max_length=2)
	interest_rate = models.DecimalField(max_digits=4,decimal_places=2)
	last_deposit = models.DateField(default=date(1970,1,1))
	guaranteed = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	creation_date = models.DateField()
	is_active = models.BooleanField(verbose_name="Active")
	is_seen = models.BooleanField(default=False)
	seen_date = models.DateField(default=None,null=True,blank=True)
	
	def last_deposit_date(self):
		if self.last_deposit == date(1970,1,1) or self.balance == 0:
			return "Pending"
		return self.last_deposit
	
	def __unicode__(self):
		return u'%s %s' % (self.account_id,self.member.first_name)
	
	def save(self, *args, **kwargs):
		if not self.account_id:
			try:				
				last_account = Savings_Account.objects.all().order_by('-id')[0]
				self.account_id = "acc-"+ str(last_account.id + 1)
			except:
				self.account_id = "acc-1"
		super(Savings_Account, self).save(*args, **kwargs)
	
class Dividends_Account(models.Model):
	dividend_id = models.CharField(max_length=10)
	member = models.ForeignKey(Member)
	amount = models.DecimalField(max_digits=20,decimal_places=2,default=0,verbose_name="Total disbursed amount")
	withdrawn = models.DecimalField(max_digits=20,decimal_places=2,default=0,verbose_name="Total withdrawn amount")
	last_amount = models.DecimalField(max_digits=20,decimal_places=2,default=0,verbose_name="Current unrecieved amount")
	last_withdrawal = models.DateField(default=None,null=True,blank=True)
	creation_date = models.DateField(default=date.today())
	is_withdrawn = models.BooleanField()
	is_seen = models.BooleanField()
	seen_date = models.DateField(default=None,null=True,blank=True)
	def __unicode__(self):
		return u'%s %s' % (self.dividend_id,self.member.first_name)
	
	def last_withdrawal_date(self):
		return "Pending" if self.last_withdrawal == None else self.last_withdrawal
	
	def save(self, *args, **kwargs):
		if not self.dividend_id:
			try:				
				last_dividend = Dividends_Account.objects.all().order_by('-id')[0]
				self.dividend_id = "div-"+ str(last_dividend.id + 1)
			except:
				self.dividend_id = "div-1"
		super(Dividends_Account, self).save(*args, **kwargs)

class Dividend(models.Model):
	amount = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	creation_date = models.DateField(default=date.today())
	total_savings = models.DecimalField(max_digits=20,decimal_places=2,default=0)
	is_applied = models.BooleanField()
	def __unicode__(self):
		return u'%d %s' % (self.amount,self.creation_date)
	
	def save(self, *args, **kwargs):
		for account in Savings_Account.objects.all():
			self.total_savings += account.balance
		super(Dividend, self).save(*args, **kwargs)
	
