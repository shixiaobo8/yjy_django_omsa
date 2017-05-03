# !/usr/bin/env python
# -*- coding:utf8 -*-
from django import forms
import re
from django.core.exceptions import ValidationError

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
