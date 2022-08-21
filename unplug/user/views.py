import re
from sys import exec_prefix
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view

from .decorator import authenticated
from .token import token_encode
import json
from .models import User, Device
from django.db import IntegrityError
from dotenv import load_dotenv
import uuid
from django.core import serializers
from electricity.models import Entries
# load .env
load_dotenv()


# Create your views here.
class LoginRequest:
    def __init__(self, body):
        self.username = body['username']
        self.password = body['password']


class JoinRequest:
    def __init__(self, body):
        self.username = body['username']
        self.password = body['password']
        self.email = body['email']
        self.name = body['name']


@api_view(['POST'])
def login(request):
    dto = LoginRequest(json.loads(request.body))
    try:
        user = User.objects.get(Q(username=dto.username) & Q(password=dto.password))
    except:
        return Response({"message": "로그인에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)

    token = token_encode(user)

    return Response({"message": "로그인에 성공했습니다.", "token": token})


@api_view(['POST'])
def join(request):
    dto = JoinRequest(json.loads(request.body))

    # validation 필요!

    # 이미 가입된 아이디인지 검증
    username_validation = User.objects.filter(username=dto.username)
    if username_validation:
        return Response({"message": "아이디가 이미 존재합니다."})

    # 이미 가입된 이메일인지 검증
    email_validation = User.objects.filter(email=dto.email)
    if email_validation:
        return Response({"message": "이메일이 이미 존재합니다."})

    user = User(username=dto.username, password=dto.password, email=dto.email, name=dto.name)

    user.save()

    return Response({"message": "회원가입에 성공했습니다!"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authenticated
def add_device(request):
    body = json.loads(request.body)
    device = body['device']
    device = Device(serial=device, user_id=request.user)
    device.save()

    return Response({"message": "디바이스 추가에 성공했습니다."})


@api_view(["GET"])
@authenticated
def get_device_list(request):
    return Response({"serial": request.user.device.serial})


@api_view(['DELETE'])
@authenticated
def user_delete(request):
    pass


@api_view(["GET"])
@authenticated
def get_friends_list(request):
    result = []
    for i in [value['username'] for value in request.user.friends.all().values()]:
        result.append(i)
    return Response(result)
    # request.user.friends.all().values()


@api_view(["GET"])
@authenticated
def get_friends_entries(request):
    result=[]
    result2=[]
    for i in [value['id'] for value in request.user.friends.all().values()]:
        devices = Device.objects.filter(user_id=User.objects.get(id=i)).values()
        if devices is not None:
            for j in devices:
                result.append(j['serial'])
    for k in result:
        result2.append((Entries.objects.filter(serial=k).values()))

    return Response(result2)



@api_view(["POST"])
@authenticated
def add_friends(request):
    pass
