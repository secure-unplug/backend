import re
from sys import exec_prefix

import jwt
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
import re
from django.core.mail import EmailMessage



load_dotenv()

import bcrypt
import logging

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



'''
@api_view(['GET'])
def send_email(request):
    email = EmailMessage(
        '가입을 축하드립니다! 지구를 지켜봐요 ^.^',
        '화이팅',  # 내용
        'yyyymimi7246@gmail.com',  # 보내는 이메일 (settings에서 설정해서 작성안해도 됨)
        to=['yyyy7246@naver.com'],  # 받는 이메일 리스트
    )
    email.send()
'''


def keyboard(request):
    return JsonResponse({

        'type': 'buttons',

        'buttons': ['로그']

    })
def message(request):

    message = ((request.body).decode('utf-8'))

    request_data = json.loads(message)

    userMessage = request_data['content']

    userType = request_data['type']



    if userMessage == '로그':

        return JsonResponse({

            'message': {

                'text': '안녕 반가워!',

            },

             'keyboard': {

                'type':'buttons',

                'buttons':['로그']

            }

        })




@api_view(['POST'])
def login(request):
    dto = LoginRequest(json.loads(request.body))
    user = User.objects.filter(username=dto.username)
    try:
        user.values()[0]['password']
    except IndexError:
        return Response({"message": "로그인에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)
    hashed_password = bytes(user.values()[0]['password'], 'utf-8')
    if not bcrypt.checkpw(bytes(dto.password, 'utf-8'), hashed_password):
        return Response({"message": "로그인에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)
    token = token_encode(user[0])

    return Response({"message": "로그인에 성공했습니다.", "token": token})


@api_view(['POST'])
def join(request):
    dto = JoinRequest(json.loads(request.body))

    # validation 필요!

    # 이미 가입된 아이디인지 검증
    username_validation = User.objects.filter(username=dto.username)
    if username_validation:
        return Response({"message": "아이디가 이미 존재합니다."},status=status.HTTP_401_UNAUTHORIZED)

    # 이미 가입된 이메일인지 검증
    email_validation = User.objects.filter(email=dto.email)
    if email_validation:
        return Response({"message": "이메일이 이미 존재합니다."}, status=status.HTTP_401_UNAUTHORIZED)
    name_validation = User.objects.filter(name=dto.name)
    if name_validation:
        return Response({"message": "이름이 이미 존재합니다."}, status=status.HTTP_401_UNAUTHORIZED)
    pwd = dto.password
    if len(pwd) < 10:
        return Response({"message": "비밀번호는 최소 10자 이상이어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    elif re.search('[0-9]+', pwd) is None:
        return Response({"message": "비밀번호는 최소 1개 이상의 숫자가 포함되어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    elif re.search('[a-zA-Z]+', pwd) is None:
        return Response({"message": "비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    elif re.search('[`~!@#$%^&*(),<.>/?]+', pwd) is None:
        return Response({"message": "비밀번호는 최소 1개 이상의 특수문자가 포함되어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    pw_hash = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt())

    user = User(username=dto.username, password=pw_hash.decode('utf-8'), email=dto.email, name=dto.name)

    #send_email(request)
    email = EmailMessage(
        '가입을 축하드립니다! 지구를 지켜봐요 ^.^',
        '조그마한 관심이 큰 결과를 만들어요~',  # 내용
        'yyyymimi7246@gmail.com',  # 보내는 이메일 (settings에서 설정해서 작성안해도 됨)
        to=[dto.email],  # 받는 이메일 리스트
    )
    user.save()
    email.send()
    return Response({"message": "회원가입에 성공했습니다!"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@authenticated
def add_device(request):
    body = json.loads(request.body)
    device = body['device']
    device = Device(serial=device, user_id=request.user, device_name=body['device_name'])
    device.save()

    return Response({"message": "디바이스 추가에 성공했습니다."})


@api_view(["GET"])
@authenticated
def get_device_list(request):
    return Response({"serial": request.user.device.serial})


@api_view(['DELETE'])
@authenticated
def user_delete(request):
    User.objects.get(username=request.user.username).delete()
    return Response({"회원탈퇴 완료"},status=status.HTTP_204_NO_CONTENT)


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
    result = []
    result2 = []
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


@api_view(["POST"])
@authenticated
def get_user_info(request):
    return Response({"name": request.user.name})


@api_view(['PUT'])
@authenticated
def update_userinfo_password(request):
    body = json.loads(request.body)
    user = User.objects.get(username=request.user.username)

    pwd = body['password']
    if len(pwd) < 10:
        return Response({"message": "비밀번호는 최소 10자 이상이어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    elif re.search('[0-9]+', pwd) is None:
        return Response({"message": "비밀번호는 최소 1개 이상의 숫자가 포함되어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    elif re.search('[a-zA-Z]+', pwd) is None:
        return Response({"message": "비밀번호는 최소 1개 이상의 영문 대소문자가 포함되어야 함"}, status=status.HTTP_401_UNAUTHORIZED)
    elif re.search('[`~!@#$%^&*(),<.>/?]+', pwd) is None:
        return Response({"message": "비밀번호는 최소 1개 이상의 특수문자가 포함되어야 함"}, status=status.HTTP_401_UNAUTHORIZED)

    pw_hash = bcrypt.hashpw(body['password'].encode('utf-8'), bcrypt.gensalt())
    user.password = pw_hash.decode('utf-8')
    user.save()

    return Response({"message": "회원 수정을 성공했습니다."})


@api_view(['PUT'])
@authenticated
def update_userinfo_username(request):
    body = json.loads(request.body)
    user = User.objects.get(username=request.user.username)  # user db
    new_name = body['name']  # put name
    if request.user.name == new_name:
        pass
    else:
        name_validation = User.objects.filter(name=new_name)
        if name_validation:
            return Response({"message": "이름이 이미 존재합니다."}, status=status.HTTP_401_UNAUTHORIZED)
    user.name = new_name


    user.save()

    return Response({"message": "회원 수정을 성공했습니다."})
