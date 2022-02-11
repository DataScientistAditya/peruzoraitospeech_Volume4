import json
from typing import Dict
from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from .serializer import Accountserializer,AuthecticationSerializer
from .models import Account
from django.views.decorators.csrf import csrf_exempt
import requests
from .backends import AccountAuth
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
import os
import time

# Create your views here.


@csrf_exempt
def Register(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        Serializer = Accountserializer(data=data)
        #print(data)
        if Serializer.is_valid():
            Email = data['email']
            User_Exist = AuthecticationSerializer.Get_User(User_Email=Email)
            print(User_Exist)
            if User_Exist is None:
                print("User not Exist")
                Serializer.save()
                Uuid = Account.objects.all().filter(email = Email).values("UUid_Token")[0]['UUid_Token']
                AccountAuth.Send_Email(Recipient=Email,Token=Uuid)
                return JsonResponse(Serializer.data, status =201)
            else:
                Dict = {"User_Exist":"Yes"}
                return JsonResponse(Dict, status =400)
        else:
            Dict_Valid = {"Not_Valid_Data":"Yes"}
            return JsonResponse(Dict_Valid, status =400)
    elif request.method == "GET":
        data = Account.objects.all()
        Serializer_get = Accountserializer(data, many=True)
        return JsonResponse(Serializer_get.data,safe=False)

@csrf_exempt
def Login(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            User_Valid = AuthecticationSerializer.Validating_User(Data=data)
            if User_Valid is not None:
                UUID_Token = Account.objects.all().filter(email=data["email"]).values("UUid_Token")[0]["UUid_Token"]
                strng=UUID_Token.hex
                request.session['uid'] = strng
                Uid =request.session['uid']
                Dict = {"Ud":Uid}
                return JsonResponse(Dict,status =201)
            else:
                Dict = {"Valid_User":"No"}
                return JsonResponse(Dict,status =400 )
        else:
            Dict = {"Valid_User":"Please Enter valid credentials"}
            return JsonResponse(Dict, status =400)


@csrf_exempt
def CompareSentences(request):
    DispalySentences = ["I Love You","I can play with the bat and ball here","The three boys like to walk to the bus stop",
    "We are sleeping We woke up late and we are very tired","Mother and father work from home. They help people and tell them what to do Some of them left their houses very early",
    "Sometimes we need to place animals into groups of same and different Together we must write the important ones on the same list"]
    if request.method == "POST":
        data = JSONParser().parse(request)
        if data is not None:
            Dict = {}
            Sentence = data["SpelledSentence"]
            Index = data["index"]
            IntIndex = int(Index)
            print("Sentence is",Sentence)
            print("Index is",IntIndex)
            SmallSentence = str(DispalySentences[IntIndex]).lower()
            Split_Original_Sentences_List = str(SmallSentence).split(" ")
            SentenceListLower = str(Sentence).lower()
            SentenceList = str(SentenceListLower).split(" ")
            Diffrence_Of_Sentences = list(set(Split_Original_Sentences_List) - set(SentenceList))
            if len(Diffrence_Of_Sentences)>0:
                Dict["Unmatched"] = Diffrence_Of_Sentences
                print(Dict)
                return JsonResponse(Dict,safe=False,status=201)
            else:
                Dict["Unmatched"] = "None"
                print(Dict)
                return JsonResponse(Dict,safe=False,status=201)
        else:
            dictError = {"Unmatched":"Not Valid Data"}
            return JsonResponse(dictError,status=401)
    else:
        dictError = {"Unmatched":"Not Valid Request"}
        return JsonResponse(dictError,status=401)

        



