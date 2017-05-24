# !/usr/bin/env python
# -*- coding:utf8 -*-
"""Myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# 登录认证
from django.contrib.auth import urls as auth_urls
from django.conf.urls import url,include
from django.contrib import admin
from learn import views as learn_views
from learn import urls
from aliyun import views as aliyun_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', learn_views.index,name='index'),
    url(r'^login$', learn_views.login),
    url(r'^register$', learn_views.register),
    url(r'^reg$', learn_views.reg),
    url(r'^ecs_list$', aliyun_views.ecs_list),
    url(r'^upload$', learn_views.upload),
    url(r'^up_recive$', learn_views.up_recive),
    url(r'^inters_data$', learn_views.inters_data,name='inters'),
    url(r'^get_imge$', learn_views.get_imge),
    url(r'^export_cvs$', learn_views.export_cvs),
    url(r'^add', learn_views.add),
]
