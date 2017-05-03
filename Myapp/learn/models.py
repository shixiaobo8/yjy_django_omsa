# !/usr/bin/env python
# -*- coding:utf8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

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
    username = models.CharField(default=False,max_length=30,unique=True)
    phone = models.CharField(default=False,max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone','username']

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
