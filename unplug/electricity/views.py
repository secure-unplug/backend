from operator import index
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import Entries
from rest_framework.views import status
from rest_framework.decorators import api_view
#from .serializers import indexserializer
import json


@api_view(['POST'])
def save_entries(request):
    body =  json.loads(request.body.decode('utf-8'))
    info = Entries(uuid = body['uuid'], watt = body['watt'])
    info.save()
    
    return Response(status=status.HTTP_201_CREATED)

