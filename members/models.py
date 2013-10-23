from django.db import models
from member import *
from datetime import *
import os
MEMBERS_PATH = os.path.abspath(os.path.dirname(__file__))

# Create your models here.
class Member(models.Model):
	LOCATIONS = (
        ('4 Kilo', '4 Kilo'),
        ('AAIT (5 Kilo)', 'AAIT (5 Kilo)'),
        ('6 Kilo', '6 Kilo'),
        ('Tikur Anbessa', 'Tikur Anbessa'),
        ('EiABC (Lideta)', 'EiABC (Lideta)'),
        ('Commerce', 'Commerce'),
        ('FBE','FBE'),
    )
	SEX = (
		('Male','Male'),
		('Female','Female'),
		)
	SUBCITY = (
		('Kolfe Keranyo','Kolfe Keranyo'),
		('Lideta','Lideta'),
		('Yeka','Yeka'),
		('Bole','Bole'),
		('Gulele','Gulele'),
		('Addis Ketema','Addis Ketema'),
		('Kirkos','Kirkos'),
		('Nefas Silk-Lafto','Nefas Silk-Lafto'),
		('Arada','Arada'),
		('Akaki Kality','Akaki Kality'),
	)
	FACULTY = (
		('Natural Science','Natural Science'),
		('Social Science','Social Science'),
		('Engineering','Engineering'),
		('Construction','Construction'),
		('Medical','Medical'),
	)
	DEPARTMENT = (
		('Computer Science','Computer Science'),
		('Chemistry','Chemistry'),
		('Physics','Physics'),
		('Biology','Biology'),
		('Statistics','Statistics'),
		('Mathematics','Mathematics'),
		('Earth Science','Earth Science'),
		('Medicine','Medicine'),		
		('Civil Engineering','Civil Engineering'),
		('Chemical Engineering','Chemical Engineering'),
		('Electrical Engineering','Electrical Engineering'),
		('Mechanical Engineering','Mechanical Engineering'),
		('Business','Business'),
		('Law','Law'),
		('History','History'),
		('Economics','Economics'),
		('Security','Security'),
		('Sanitation','Sanitation'),
		('Registrar','Registrar'),
		('Dormitory','Dormitory'),
	)
	
	EMPLOYMENT = (
	('Permanent','Permanent'),
	('Contract','Contract'),
	)
	
	member_id = models.CharField(max_length=20,blank=True)
	photo = models.ImageField(upload_to="home/waq/Documents/photos/",default=None,null=True,verbose_name="Photo Location")
	university_id = models.CharField(max_length=20)
	first_name = models.CharField(max_length=50)
	father_name = models.CharField(max_length=50)
	grand_father_name = models.CharField(max_length=50)
	subcity = models.CharField(max_length=100, choices=SUBCITY)
	wereda = models.CharField(max_length=10)
	house_number = models.CharField(max_length=5)
	house_phone_number = models.CharField(max_length=13,blank=True,null=True)
	office_phone_number = models.CharField(max_length=13)
	cell_phone_number = models.CharField(max_length=13,blank=True,null=True)
	POBox = models.CharField(max_length=10,blank=True,null=True)
	birth_date = models.DateField(blank=True,null=True)
	sex = models.CharField(max_length=6, choices=SEX)
	campus = models.CharField(max_length=100,choices=LOCATIONS)
	faculty = models.CharField(max_length=100, choices=FACULTY)
	department = models.CharField(max_length=100, choices=DEPARTMENT)
	salary = models.DecimalField(max_digits=8, decimal_places=2)
	employment_type = models.CharField(max_length=20,choices=EMPLOYMENT)
	email = models.EmailField(blank=True,null=True,max_length=200)
	savings_percentage = models.DecimalField(max_digits=5, decimal_places=2)
	application_date = models.DateField(default=date.today())
	is_registered = models.BooleanField(verbose_name="Registered")
	registration_date = models.DateField(blank=True,null=True,default=None)
	
	def display_photo(self):
		if self.photo:
			return u'<img src="%s" width="25" height="25" />' % self.photo.url
		else:
			return 'No picture'
	display_photo.short_description = 'Photo'
	display_photo.allow_tags = True
	
	def display_big_photo(self):
		if self.photo:
			return u'<img src="%s" width="150" height="150" />' % self.photo.url
		else:
			return 'No picture'
	display_big_photo.short_description = 'Photo'
	display_big_photo.allow_tags = True
	
	def __unicode__(self):
		return u'%s %s %s' % (self.first_name,self.father_name,self.grand_father_name)
	
	"""def save(self, *args, **kwargs):
		if not self.id:
			try:				
				last_member = Member.objects.all().order_by('-id')[0]
				self.member_id = str("mem-"+last_member.id + 1)
			except:
				self.member_id = "mem-1"
		super(Member, self).save(*args, **kwargs) 
"""
class Notification(models.Model):
	notification_id = models.CharField(max_length=10,blank=True)
	message = models.TextField()
	to = models.ForeignKey(Member)
	sent_date = models.DateField()
	def __unicode__(self):
		return u'%s %s' % (self.to.first_name,self.message)
	
	def save(self, *args, **kwargs):
		if not self.notification_id:
			try:				
				last_notification = Notification.objects.all().order_by('-id')[0]
				self.notification_id = "not-"+ str(last_notification.id + 1)
			except:
				self.notification_id = "not-1"
		super(Notification, self).save(*args, **kwargs)
