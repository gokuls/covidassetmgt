# -*- coding: utf-8 
from __future__ import unicode_literals

from django.db import models

# Create your models here.


from datetime import datetime
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import User

from django.contrib import admin








class State(models.Model):
    state_id  			= models.BigAutoField(primary_key=True)
    state_name			= models.CharField(max_length=250,unique=True)
    creation_date		= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.state_name



class District(models.Model):
    district_id			= models.BigAutoField(primary_key=True)
    district_name		= models.CharField(max_length=250,unique=True)
    state_id 			= models.ForeignKey(State,on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.district_name


class Hospital(models.Model):
	hospital_id				= models.BigAutoField(primary_key=True)
	district_id 			= models.ForeignKey(District,on_delete=models.CASCADE)
	hospital_name			= models.CharField(max_length=250)
	hospital_type			= models.CharField(max_length=250)
	address 				= models.CharField(max_length=250)
	contact_number			= models.CharField(max_length=250)
	city					= models.CharField(max_length=250,blank=True,null=True)
	taluk 	 				= models.CharField(max_length=250,blank=True,null=True)
	pincode	 				= models.CharField(max_length=250,blank=True,null=True)
	doctors					= models.IntegerField()
	healthworkers			= models.IntegerField()
	latitude 				= models.CharField(max_length=250)
	longitude 				= models.CharField(max_length=250)
	creation_date 			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.hospital_name


class Asset(models.Model):
    asset_id			= models.BigAutoField(primary_key=True)
    asset_name			= models.CharField(max_length=250,unique=True)
    author 				= models.ForeignKey(User,on_delete=models.CASCADE)
    creation_date 		= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.asset_name


class AssetMgt(models.Model):
	asset_id 			= models.ForeignKey(Asset,on_delete=models.CASCADE)
	hospital_id 		= models.ForeignKey(Hospital,on_delete=models.CASCADE)
	author 				= models.ForeignKey(User,models.SET_NULL,blank=True,null=True)
	asset_total			= models.IntegerField()
	asset_utilized 		= models.IntegerField(null=True,default=0)
	asset_balance 		= models.IntegerField(null=True,default=0)
	creation_date 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.asset_id.asset_name


class PatientStat(models.Model):
	hospital_id 		= models.ForeignKey(Hospital,on_delete=models.CASCADE)
	author 				= models.ForeignKey(User,models.SET_NULL,blank=True,null=True)
	patient_count		= models.IntegerField(default=0)
	creation_date 		= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "%d-patients"%self.patient_count


class UserProfile(models.Model):
	user 				= models.OneToOneField(User, on_delete=models.CASCADE)
	state_id 			= models.ForeignKey(State,on_delete=models.CASCADE)
	district_id			= models.ForeignKey(District,on_delete=models.CASCADE)
	hospital_id			= models.ForeignKey(Hospital,models.SET_NULL,blank=True,null=True)
	adminstate 			= models.IntegerField()
	creation_date 		= models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.user.username
