from operator import index
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import Entries
from rest_framework.views import status
from rest_framework.decorators import api_view
#from .serializers import indexserializer
import json
from datetime import datetime


@api_view(['POST'])
def save_entries(request):
    body =  json.loads(request.body.decode('utf-8'))
    info = Entries(uuid = body['uuid'], watt = body['watt'])
    info.save()
 
    return Response(status=status.HTTP_201_CREATED)

@api_view(['GET'])
def view_entries(request):
    uuid = "asde"           ##request.user.uuid 이런식으로 uuid 받아오기.
    body =  json.loads(request.body.decode('utf-8'))

    start_date = datetime.strptime(body['start_date'], "%Y-%m-%d")
    end_date = datetime.strptime(body['end_date'], "%Y-%m-%d")


    data = Entries.objects.filter(uuid=uuid, created_at__range=(start_date, end_date)).order_by('-created_at', '-id')
    
    return Response(data.values())
    
