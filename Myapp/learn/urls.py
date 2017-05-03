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
from aliyun import views as aliyun_views

urlpatterns = [
    url(r'^auth/', include('Myapp.urls')),
    url(r'^ecs_list$', aliyun_views.ecs_list),
]
