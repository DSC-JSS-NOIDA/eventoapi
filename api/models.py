# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.contrib.auth.models import  AbstractUser
from django.contrib.auth import get_user_model
User = get_user_model()



class Society(models.Model):
	name              = models.CharField(max_length=100,null=False)
	created_at 		  = models.DateTimeField(default=timezone.now())
	logo              = models.ImageField(upload_to='',blank=True)
	department_name   = models.CharField(max_length=120,null=False)
	contact_no        = models.IntegerField(max_length=10,null=False)
	email		      = models.TextField(max_length=100,null=False)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name	



class Tag(models.Model):
	name 	= models.CharField(max_length=100,null=False)

	def __str__(self):
		return self.name

class Event(models.Model):
	name      	   = models.TextField(max_length=150,null=False)
	start_day  	   = models.DateTimeField(u'Start day of the event', help_text=u'Start day of the event')
	end_day    	   = models.DateTimeField(u'End day of the event', help_text=u'End day of the event')
	start_time	   = models.TimeField(u'Starting time', help_text=u'Starting time')
	end_time  	   = models.TimeField(u'Ending time', help_text=u'Ending time')
	notes          = models.TextField(u'Textual field', help_text=u'Textual field', blank=True,null=True)
	image     	   = models.ImageField(upload_to='', blank=True)
	contact_person = models.IntegerField(max_length=10,null=False)
	contact_person = models.IntegerField(max_length=10,null=False)
	society        = models.ForeignKey(Society, related_name='event', on_delelte=models.CASCADE)
	creater        = models.ForeignKey(User, related_name='event' , on_delelte=models.CASCADE)

	def __str__(self):
		return self.event

class User(models.Model):
	name       = models.CharField(max_length=100,blank=False,null=False)
	otp        = models.IntegerField(max_length=15,null=True)
	otp_expiry = models.DateTimeField(default=timezone.now())
    role	   = models.CharField(max_length=20, null=False)
    contact_no = models.IntegerField(max_length=10,null=True)
    status     = models.IntegerField(max_length=10)






