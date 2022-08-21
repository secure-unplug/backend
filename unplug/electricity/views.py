from operator import index
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import Entries
from rest_framework.views import status
from rest_framework.decorators import api_view
# from .serializers import indexserializer
import json
from datetime import datetime
from .models import Metadata
from .elec_calc import calc
from user.decorator import authenticated
from user.models import User


@api_view(['POST'])
#@authenticated
def save_entries(request):
    body = json.loads(request.body.decode('utf-8'))
    info = Entries(serial=body['serial'], watt=body['watt'])
    info.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authenticated
def view_entries(request):
    #uuid = request.user.uuid #이런식으로 uuid 받아오기.
    #print(uuid)
    device = request.user.device
    print(device)
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    data = Entries.objects.filter(serial=device, created_at__range=(start_date, end_date)).order_by('-created_at', '-id')

    return Response(data.values())


@api_view(['GET'])
@authenticated
def view_average(request):
    month = request.GET['month']
    data = Metadata.objects.filter(month=month)
    fee, tex_1, tex_2, total = calc((data.values()[0]['average_Kwatt']))
    money = dict(fee=fee, tex_1=tex_1, tex_2=tex_2, total=total)
    # return Response(data.values())
    return Response(money)

@api_view(['GET'])
@authenticated
def view_device_data(request):
    return Response([{"serial": value['serial']} for value in request.user.device.all().values()])


@api_view(['GET'])
@authenticated
def view_my_entries(request):
    result = []
    for i in [value['serial'] for value in request.user.device.all().values()]:
        result.append(Entries.objects.filter(serial=i).values())
    return Response(result)
