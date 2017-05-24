# !/usr/bin/env python
# -*- coding:utf8 -*-
from django import forms
import re
from django.core.exceptions import ValidationError
from django.forms.extras.widgets import SelectDateWidget

YEARS_CHOICES = ('2016','2017')
MONTHS_CHOICES = ('01','02','03','04','05','06','07','08','09','10','11','12')
DAYS_CHOICES = ('01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31')
#DAYS = [ i for i in range(12,32) ]
#DAYS_CHOICES = MONTHS_CHOICES+tuple(DAYS)

class UserInfo(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	phone = forms.CharField(required=True)
	
def PhoneValidate(value):
	phone_re = re.compile(r'^(13[0-9]|15[012356789]|17[0678]|18[0-9]|14[57])[0-9]{8}$')
	if not phone_re.match(value):
		raise ValidationError('手机格式错误')

class NewForm(forms.Form):
	username = forms.CharField(label='用户名',max_length=16,error_messages={'required':"用户名不能为空"},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用户名'},),)
	password = forms.CharField(max_length=100,error_messages={'required':"密码不能为空"},widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码'},),)
	phone = forms.CharField(validators=[PhoneValidate,],error_messages={'required':'手机号码不能为空'},
	widget=forms.TextInput(attrs={'class':'form-control','placeholder':'手机号'},),)
	email = forms.EmailField(required=True,label='电子邮箱',max_length=100,error_messages={'required':'邮箱不能为空!'},widget=forms.TextInput(attrs={'class':'form-control','placeholder':'email'},))

class LoginForm(forms.Form):
	username = forms.CharField(label='用户名',max_length=16,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用户名'},),)
	password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码'},),)

class intersForm(forms.Form):
	date = forms.DateField(label='请选择日期',widget=SelectDateWidget(years=YEARS_CHOICES))
	top = forms.CharField(label='请填写查询的top条数',max_length=160,widget=forms.TextInput,)
	#month = forms.DateField(label='请选择月份',widget=SelectDateWidget(months=MONTHS_CHOICES))
	#day = forms.DateField(label='请选择日期',widget=SelectDateWidget(days=DAYS_CHOICES))
