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
from dateutil.relativedelta import relativedelta
import re




@api_view(['POST'])
# @authenticated
def save_entries(request):
    valid_uuid = re.compile('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
    body = json.loads(request.body.decode('utf-8'))
    info = Entries(serial=body['serial'], watt=body['watt'])
    if valid_uuid.search(body['serial']) is None:
        return Response({"Not in valid serial format"})
    if type(body['watt']) != int:
        return Response({"watt is not integer type"})
    info.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authenticated
def view_entries(request):

    device_list = [value['serial'] for value in request.user.device.all().values()]
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    
    # date 포맷 유효성 검사
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return Response({"Not in valid date format"})
    try:
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return Response({"Not in valid date format"})
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    data = []
    for i in device_list:
        data.append(Entries.objects.filter(serial=i, created_at__range=(start_date, end_date)).order_by('-created_at',
                                                                                                        '-id').values())

    return Response(data)

'''
@api_view(['GET'])
@authenticated
def export_exel(request):
    device_list = [value['serial'] for value in request.user.device.all().values()]
    #print(device_list)
    data = []
    for i in device_list:
        data.append(Entries.objects.filter(serial=i).values())
    #print(data)
    #print(request.user.device.all().values())
    
    #print(data)
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'example.xls' 
    wb = xlwt.Workbook(encoding='utf-8') #encoding은 ansi로 해준다.
    ws = wb.add_sheet('전력량') #시트 추가

    title_style = xlwt.easyxf('pattern: pattern solid, fore_color indigo; align: horizontal center; font: color_index white;')
    data_style = xlwt.easyxf('align: horizontal right')

    row_num = 0
    col_names = ['serial', 'watt', 'created_at']
    rows = []
    df = pd.DataFrame.from_records(data)
    rows=df
    print(df)
    # for datum in df:
    #     rows.append(int(datum['id']), datum['serial'], datum['watt'], datum['created_at'])
    # 첫번째 열: 설정한 컬럼명 순서대로 스타일 적용하여 생성
    row_num = 0
    for idx, col_name in enumerate(col_names):
        ws.write(row_num, idx, col_name)
    
    # 두번째 이후 열: 설정한 컬럼명에 맞춘 데이터 순서대로 스타일 적용하여 생성
    for row in rows:
        row_num +=1
        for col_num, attr in enumerate(row):
            ws.write(row_num, col_num, attr)
    
    wb.save(response)
    print(rows)
    return response
'''
@api_view(['GET'])
@authenticated
def view_period_average(request):
    device_list = [value['serial'] for value in request.user.device.all().values()]
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    serial = request.GET['serial']

    # date 포맷 유효성 검사
    try:
        datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        return Response({"Not in valid date format"})
    try:
        datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return Response({"Not in valid date format"})
    # serial 포맷 유효성 검사
    valid_uuid = re.compile('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
    if valid_uuid.search(serial) is None:
        return Response({"Not in valid serial format"})
    

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    dates = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end_date - start_date).days + 1)]
    data = []
    for date in dates:
        date1 = datetime.strptime(date, "%Y-%m-%d")
        date2 = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)
        data.append(Entries.objects.filter(serial=serial, created_at__range=(date1, date2)).order_by('-created_at',
                                                                                                     '-id').values())
    return Response(data)


@api_view(['GET'])
@authenticated
def view_device_fee(request):
    today = datetime.now()
    serial = request.GET['serial']
    # serial 포맷 유효성 검사
    valid_uuid = re.compile('[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}')
    if valid_uuid.search(serial) is None:
        return Response({"Not in valid serial format"})
    total_watt = 0
    month_first = datetime(today.year, today.month, 1).strftime("%Y-%m-%d")
    month_last = (datetime(today.year, today.month, 1) + relativedelta(months=1) - relativedelta(seconds=1)).strftime(
        "%Y-%m-%d")
    data = Entries.objects.filter(serial=serial, created_at__range=(
        month_first, month_last)).order_by(
        '-created_at',
        '-id')
    j = 0
    for i in data:
        total_watt += data[j].watt
        j += 1
    fee = calc(total_watt / 1000)
    return Response(fee)


@api_view(['GET'])
@authenticated
def view_average_kwatt(request):
    month = int(str(datetime.now().strftime("%m")).replace('0', ''))
    return Response(Metadata.objects.filter(month=month).values('average_Kwatt'))


@api_view(['GET'])
@authenticated
def view_average_money(request):
    # month 포맷 유효성 검사
    month = request.GET['month']
    try:
        datetime.strptime(month, '%m')
    except ValueError:
        return Response({"Not in valid month format"})
    data = Metadata.objects.filter(month=month)
    fee, tex_1, tex_2, total = calc((data.values()[0]['average_Kwatt']))
    money = dict(fee=fee, tex_1=tex_1, tex_2=tex_2, total=total)
    # return Response(data.values())
    return Response(money)


@api_view(['GET'])
@authenticated
def view_device_data(request):
    return Response([{"serial": value['serial'], "device_name": value['device_name']} for value in
                     request.user.device.all().values()])



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
    device_list = [value['serial'] for value in request.user.device.all().values()]
    earth_level = []
    total_watt = 0
    day_average = (day_average * 1000)
    # day_average는 kwh단위, w * 3600 = kwh
    print(day_average)
    j = 0
    for i in device_list:
        data = Entries.objects.filter(serial=device_list[j], created_at__range=(
            datetime.now().strftime("%Y-%m-%d"), (today + timedelta(days=1)).strftime("%Y-%m-%d"))).order_by(
            '-created_at',
            '-id')
        for t in data:
            total_watt += t.watt/20
        print(total_watt)
        j += 1
        if day_average * 1.4 < total_watt:
            earth_level.append(5)
        elif day_average * 1.2 < total_watt <= day_average * 1.4:
            earth_level.append(4)
        elif day_average < total_watt <= day_average * 1.2:
            earth_level.append(3)
        elif day_average * 0.8 < total_watt <= day_average:
            earth_level.append(2)
        elif day_average * 0.6 < total_watt <= day_average * 0.8:
            earth_level.append(1)
        elif total_watt <= day_average * 0.6:
            earth_level.append(1)
        print(total_watt)
        total_watt = 0
    # total_kwatt = total_watt / 1000

    '''
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
    elif total_kwatt <= day_average * 0.6:
        earth_level=1
    '''
    return Response(earth_level)
