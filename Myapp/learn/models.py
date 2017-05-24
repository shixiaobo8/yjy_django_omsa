# !/usr/bin/env python
# -*- coding:utf8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.backends import ModelBackend

# 自定义认证后端类
class Myauthbackend(ModelBackend):
	def get_user(self,user_id):
		try:
			return Myuser.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

	# 基于用户名密码的验证
	def authenticate(username=None,password=None):
		try:
			pwd = Myuser.check_password(password)
			user = MyUser.objects.get(username=username)
			if user:
				pwd = Myuser.check_password(password)
				if pwd:
					return user
				else:
					return None
			else:
				return None
	
		except Myuser.DeosNotExist:

			pass
	
	# 基于token的验证
	#def authenticate(self,token=None):
	#	pass

# 扩展User类
class MyUserManager(BaseUserManager):
    def create_user(self, email, phone,username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not phone:
            raise ValueError('Users must have an email phone')
        
	user = self.model(
            email=self.normalize_email(email),
            phone=phone,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone,username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            username=username,
            password=password,
            phone=phone
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
    )
    #user = models.OneToOneField(User)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    username = models.CharField(default=False,max_length=30,unique=True)
    phone = models.CharField(default=False,max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone','email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_user_model():
	try:
		return django_apps.get_model(settings.AUTH_USER_MODEL)
	except ValueError:
        	raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    	except LookupError:
        	raise ImproperlyConfigured("AUTH_USER_MODEL refers to model '%s' that has not been installed" % settings.AUTH_USER_MODEL)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Nav(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=40,default="导航栏")
	nnav = models.CharField(max_length=40,default="二级分类")
	nnav_url = models.CharField(max_length=40,default="#")
	link = models.CharField(max_length=40,default='#')

	def __unicode__(self):
		return self.name
