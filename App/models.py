import uuid
from django.db import models
from django import forms
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.forms import forms
from django.db.models.fields import CharField, EmailField
from django.core.exceptions import ValidationError
from django.forms import widgets
from django.forms.widgets import Widget
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,PermissionsMixin, User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
import datetime

# Create your models here.
class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class Account(AbstractBaseUser):
    email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 				= models.CharField(max_length=30)
    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)
    is_email_varified		= models.BooleanField(default=False)
    UUid_Token		= models.UUIDField(default=str(uuid.uuid4()), editable=False)
	

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
