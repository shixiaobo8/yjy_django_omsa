#! /usr/bin/env python
# -*- coding:utf8 -*-

from django.http import HttpResponse,StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NewForm, LoginForm, intersForm
from .models import Nav
from .models import MyUser
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
from django.db import connection
from django.core import serializers
from django.conf import settings
import os,json
import xlwt
from urllib import *

def inters_count(date_table,top):
	"""
		date_table: 形如2017_05_13
		top: 查询的条数
	"""
	import  MySQLdb as mdb
	import datetime
	db_conn = mdb.connect('59.110.11.16','web_data','web_data@2017','all_web_data_history')
	cursor = db_conn.cursor()
	ret = ''
	try:
		cursor.execute("select * from (select `key`,`requests` from "+date_table+"_history_data limit "+top+") as top order by `requests`+0 desc limit "+top+";")
		datas = cursor.fetchall()
		ret = datas
		#return HttpResponse(ret)
		#data_js = dict()
		#for data in datas:
		#	data_js[data[0]] = data[1]
	except mdb.Error,e:
		print e
		#db_conn.close()
	db_conn.close()
	# 内部调用数据返回
	return ret
	# 外部调用接口数据返回
	#return render(request,'inters_count.html',{'data':datas})
	#return render(request,'inters_count.html',{'data':data_js})
	
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

def inters_data(request):
	d = ['1','2','3','4','5','6','7','8','9']
	err_mess = '对不起没有改时段的接口信息!'
	if request.method == 'GET':
		form = intersForm(request.GET)
		f_data = request.GET
		if f_data:
			d_date = f_data['data[d]']
			top = f_data['data[top]']
			g_data = inters_count(d_date,top)
			if f_data['action'] == 'cvs' and g_data:
				# 自定义httpResponse流
				xls_name = 'd_date.xls'
				response = HttpResponse(content_type='application/vnd.ms-excel;charset=utf-8')
				response['mimetype']='application/vnd.ms-excel'
				response['Content-Disposition'] = 'attachment; filename=' + d_date + '.xls'
				# 创建工作簿
				workbook = xlwt.Workbook(encoding='utf-8')
				# 创建工作页
				sheet1 = workbook.add_sheet(d_date+u'访问情况')
				# 开始写入excel
				row0 = [u'访问url',u'访问次数']
				#for i in range(0,len(row0)):
				sheet1.write(0,0,row0[0])
				sheet1.write(0,1,row0[1])
				for i in range(1,len(g_data)):
					sheet1.write(i,0,g_data[i][0])
					sheet1.write(i,1,g_data[i][1])
				workbook.save(response)
				return response
			elif f_data['action'] == 'imge' and g_data:
				pass
			else:
				return HttpResponse('检索的数据不存在')
		else:
			return render(request,'inters_count.html',{'form':form})

	if request.method == 'POST':
		form = intersForm(request.POST)
		data = form.data
		date_year = data['date_year']
		date_month = data['date_month']
		date_day = data['date_day']
		d_date = date_year + date_month + date_day
		top  = data['top']
		if  d_date is None or top is None:
			return HttpResponse(err_mess)
			return render(request,'inters_count.html',{'form':form,'error_mess':err_mess })
		else:
			if d_date is not None and top is not None:
				if date_day in d:
					date_day = '0' + date_day
				if date_month in d:
					date_month = '0' + date_month
				d_date = date_year + '_' + date_month + '_' + date_day
				datas = inters_count(d_date,top)	
				#return HttpResponse(datas)
				if datas:
					return render(request,'inters_count.html',{'form':form,'data':datas})
				else:
					return render(request,'inters_count.html',{'form':form,'error_mess':err_mess })

def export_cvs(request):
	if request.method == 'GET':
		form = intersForm(request.GET)
		f_data = json.loads(request.GET.items()[0][1])
		if f_data:
			d_date = f_data['d']
			top = f_data['top']
			g_data = inters_count(d_date,top)
			if  g_data:
				# 自定义httpResponse流
				# response = HttpResponse(content_type='application/vnd.ms-excel;charset=utf-8')
				response = HttpResponse(content_type='application/octet-stream;charset=utf-8')
				response['mimetype']='application/octet-stream'
				response['Content-Disposition'] = 'attachment; filename=' + d_date + '.xls'
				workbook = xlwt.Workbook(encoding='utf-8')
				# 创建工作页
				sheet1 = workbook.add_sheet(d_date+u'访问情况')
				# 开始写入excel
				row0 = [u'访问url',u'访问次数']
				sheet1.write(0,0,row0[0])
				sheet1.write(0,1,row0[1])
				for i in range(1,len(g_data)):
					sheet1.write(i,0,g_data[i][0])
					sheet1.write(i,1,g_data[i][1])
				workbook.save(response)
				url = request.get_full_path()
				return response
				#return HttpResponse([{'url':url,'response':response}])
			else:
				return HttpResponse('检索的信息不存在')

def get_imge(request):
	return HttpResponse('頁面正在開發中。。。')

def add(request):
	if request.method == 'GET':
		data = request.GET
		if data:
			return HttpResponse(int(data['a'])+int(data['b']))
		else:
			return render(request,'add.html')
	

class SettingsBackend(object):
    """
    Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.

    Use the login name, and a hash of the password. For example:

    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'sha1$4e987$afbcf42e21bd417fb71db8c66b321e9fc33051de'
    """
    def check_password(self,password):
	pass

    def authenticate(self, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = MyUser.objects.get(username=username)
            except MyUser.DoesNotExist:
                # Create a new user. Note that we can set password
                # to anything, because it won't be checked; the password
                # from settings.py will.
                user = MyUser(username=username, password='get from settings.py')
                user.is_staff = True
                user.is_superuser = True
                user.save()
            return user
        return None

    def get_user(self, user_id):
        try:
            return MyUser.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

