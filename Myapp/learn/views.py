#! /usr/bin/env python
# -*- coding:utf8 -*-

from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
#from django.forms.models import model_to_dict
from .forms import NewForm, LoginForm
from .models import Nav
from .models import MyUser
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.db import connection
from django.core import serializers
from django.contrib.auth.models import User
import os

def reg(request):
	form = NewForm(request.POST)
	return render(request,'register.html',{'form':form})

def index(request):
	form = LoginForm(request.POST)
	navs = list(Nav.objects.all())
	return render(request,'login.html',{'navs':navs,'form':form})

#def login(request):
#	if request.method == 'POST':
#		form = LoginForm(request.POST)
#		data = form.data
#		username = data['username']
#		password = data['password']
#		user = User.objects.filter(username=username,password=password)
#		#user = User.objects.get(username=username,password=password)
#		if user:
#			user = list(user.values('username','email'))[0]
#			return render(request,'user.html',{'user':user})
#		else:
#			login_mess = '用户名或者密码不正确'
#			return render(request,'login.html',{'form':form,'login_mess':login_mess})
#	else:
#		login_mess = 'method not allowed '
#		return render(request,'login.html',{'form':form,'login_mess':login_mess})

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		#data = form.data
		username = form.data['username']
		password = form.data['password']
		if form.is_valid():
			#return HttpResponse(data.items())
			user = authenticate(username=username,password=password)
			return HttpResponse(user)
			if user is not None and user.is_active:
				login(request,user)
				return render(request,'user.html',{'user':user})
			else:
				login_mess = '用户名或者密码不正确'
				return render(request,'login.html',{'form':form,'login_mess':login_mess})
	else:
		login_mess = 'http method not allowed'
		return render(request,'login.html',{'form':form,'login_mess':login_mess})
		

def register(request):
	if request.method == 'POST':
		form = NewForm(request.POST)
		if form.is_valid():
            # message = "<h2 style='color:red;'>  your actually are my love ! i do mybest ! i will love you the rest of my life ! </h2>"
			data = form.data
			if  MyUser.objects.filter(username=data['username']):
				reg_error = '用户名已存在!'
				return render(request,'register.html',{'reg_error':reg_error,'form':form})
			else:
				#User.objects.create_user(username=data['username'],password=data['password'],email=data['email'],phone=data['phone'])
				user = MyUser()
				user.set_password(data['password'])
				user.username = data['username']
				user.phone = data['phone']
				user.email = data['email']
				user.save()
				return HttpResponseRedirect('/ecs_list')
				#return HttpResponse('注册成功!!')
		else:
			message = "<b style='color:red;'>invalid</b> please keep slient and keep friendship and keep smile ^_^ and keep doing yourself and belive yourself ! "
			reg_error = form.errors
			return render(request,'register.html',{'message':message,'reg_error':reg_error,'form':form })
	if request.method == 'GET':
		return HttpResponse(form.data)
		form = NewForm(request.POST)
		return HttpResponseRedirect(request,'/register.html',{'form':form})
		
def upload(request):
	#if request.method == 'GET':
	form = NewForm(request.GET)
	return render(request,'upload.html')

def up_recive(request):
	if request.method == 'POST':
		files = request.FILES.get("up_file",None) # 获取上传的文件,如果没有文件,则默认为None
		if not files:
			return HttpResponse("没有上传数据")
		save_destination = open(os.path.join("uploads",files.name),'wb+') # 打开特定的文件进行二进制写操作
		for chunk in files.chunks():
			save_destination.write(chunk)
		save_destination.close()
		return HttpResponse("上传完毕!")

