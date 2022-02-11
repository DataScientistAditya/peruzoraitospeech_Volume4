from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from .models import Account
from django.core.mail import send_mail
from django.conf import settings
import os
from datetime import datetime
import shutil
import json
import requests
from urllib import parse, request


class AccountAuth(ModelBackend):

    def authenticate(Username=None, Password = None):
        UserModel = get_user_model()
        if Username is not None:
            try:
                id = UserModel.objects.all().filter(email = Username).values("id")[0]["id"]
            except:
                return None
        if id is not None:
            try:
                user_pass = UserModel.objects.all().filter(id = id).values("password")[0]['password']
                if user_pass == Password:
                    return id
            except:
                return None
        
        else:
            return None
    
    def get_user(self,id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk= id) # <-- must be primary key and number
        except User.DoesNotExist:
            return None

    def Send_Email(Recipient, Token):
        Subject = "MightyNeurons Email Verification"
        Message = f"Your Account Needs to Be Verified http://localhost:3000/Verify/{Token}"
        Email_Sender = settings.EMAIL_HOST_USER
        Email_Reciever = [Recipient]
        send_mail(subject=Subject, message=Message, from_email=Email_Sender, recipient_list=Email_Reciever)
    