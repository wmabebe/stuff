from django.db import models

# Create your models here.
class Constant(models.Model):
	savings_interest_rate = models.DecimalField(max_digits=4,decimal_places=2)
	loan_interest_rate = models.DecimalField(max_digits=4,decimal_places=2)
	def __unicode__(self):
		return "Constants"
