def calc(electronic):
    kWh = electronic
    fee = 0
    tex_1 = 0
    tex_2 = 0
    total = 0
    if 0 <= kWh <= 100:
        fee = kWh * 60.7 + 410

    elif 101 <= kWh <= 200:
        fee = (kWh - 100) * 125.9 + 6070 + 910

    elif 201 <= kWh <= 300:
        fee = (kWh - 200) * 187.9 + 18660 + 1600

    elif 301 <= kWh <= 400:
        fee = (kWh - 300) * 280.6 + 37450 + 3850

    elif 401 <= kWh <= 500:
        fee = (kWh - 400) * 417.7 + 65510 + 7300

    elif kWh >= 501:
        fee = (kWh - 500) * 709.5 + 107280 + 12940
    # 부가가치세 원 미만 사사오입 절사
    tex_1 = round(fee * 0.1)
    # 전력산업기반기금 10원 미만 절사
    tex_2 = int(fee * 0.037) - (int(fee * 0.037) % 10)
    # 총 전기요금 10원 미만 절사
    total = int(fee + tex_1 + tex_2) - (int(fee + tex_1 + tex_2) % 10)
    return fee, tex_1, tex_2, total
    '''
    print("전기 사용료 : " + str(int(fee)) + "원")
    print("부가가치세 : " + str(tex_1) + "원")
    print("전력산업기반기금 : " + str(tex_2) + "원")
    print("총 합 요금 : " + str(total) + "원")
    '''
