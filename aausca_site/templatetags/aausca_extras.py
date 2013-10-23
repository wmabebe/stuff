from django.template import Library
from datetime import date

register = Library()

@register.filter
def up_to_now( value ):
	return range(value,date.today().year)
@register.filter
def get_range(value):
	return range(value)
@register.filter
def up_to_hundred( value ):
	return range(value,101)
@register.filter
def repayment_months( value ):
	return range(1,value)