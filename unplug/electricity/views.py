from operator import index
from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from .models import Entries
from rest_framework.views import status
from rest_framework.decorators import api_view
# from .serializers import indexserializer
import json
from datetime import datetime, timedelta
from .models import Metadata
from .elec_calc import calc
from user.decorator import authenticated
from user.models import User



@api_view(['POST'])
# @authenticated
def save_entries(request):
    body = json.loads(request.body.decode('utf-8'))
    info = Entries(serial=body['serial'], watt=body['watt'])
    info.save()

    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authenticated
def view_entries(request):
    print(request.user)
    device = request.user.device.values()[0]['serial']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    data = Entries.objects.filter(serial=device, created_at__range=(start_date, end_date)).order_by('-created_at','-id')

    return Response(data.values())


@api_view(['GET'])
@authenticated
def view_average_kwatt(request):
    month = int(str(datetime.now().strftime("%m")).replace('0', ''))
    return Response(Metadata.objects.filter(month=month).values('average_Kwatt'))


@api_view(['GET'])
@authenticated
def view_average_money(request):
    month = request.GET['month']
    data = Metadata.objects.filter(month=month)
    fee, tex_1, tex_2, total = calc((data.values()[0]['average_Kwatt']))
    money = dict(fee=fee, tex_1=tex_1, tex_2=tex_2, total=total)
    # return Response(data.values())
    return Response(money)


@api_view(['GET'])
@authenticated
def view_device_data(request):
    return Response([{"serial": value['serial'], "device_name": value['device_name']} for value in request.user.device.all().values()])


@api_view(['GET'])
@authenticated
def view_my_entries(request):
    result = []
    for i in [value['serial'] for value in request.user.device.all().values()]:
        result.append(Entries.objects.filter(serial=i).values())
    return Response(result)

@api_view(['GET'])
@authenticated
def get_kwatt_level(request):
    month = int(str(datetime.now().strftime("%m")).replace('0', ''))
    today = datetime.now()
    kwatt = Metadata.objects.filter(month=month).values()[0]['average_Kwatt']
    day_average = float(kwatt / 30)
    device = request.user.device.values()[0]['serial']
    data = Entries.objects.filter(serial=device, created_at__range=(
        datetime.now().strftime("%Y-%m-%d"), (today + timedelta(days=1)).strftime("%Y-%m-%d"))).order_by('-created_at',
                                                                                                         '-id')
    earth_level = 0
    total_watt = 0
    for i in data:
        total_watt += i.watt
    total_kwatt = total_watt / 1000
    print(day_average)
    print(total_kwatt)
    if day_average * 1.4 < total_kwatt:
        earth_level = 5
    elif day_average * 1.2 < total_kwatt <= day_average * 1.4:
        earth_level = 4
    elif day_average < total_kwatt <= day_average * 1.2:
        earth_level = 3
    elif day_average * 0.8 < total_kwatt <= day_average:
        earth_level = 2
    elif day_average * 0.6 < total_kwatt <= day_average * 0.8:
        earth_level = 1
    return Response(earth_level)

