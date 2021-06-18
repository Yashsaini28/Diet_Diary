from os import linesep
from pandas.core.frame import DataFrame
from rest_framework.response import Response
from bs4 import BeautifulSoup
import urllib.request as urllib2
import re
from rest_framework.views import APIView
from django.views.generic import View
from urllib.request import urlopen
from json import dumps
import json
import requests
from django.template import RequestContext
from FoodIndex_new.models import *
import matplotlib.pyplot as plt1
from django.db.models import Sum
import seaborn as sns
from matplotlib import pyplot as plt, use
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.contrib import messages
from home_app_new.models import Main_page
from basic_app_new.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from datetime import datetime, date
import datetime as dt
from django.urls import reverse
import mysql.connector as msql
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('Agg')
#from requests.api import request

# Create your views here.
user_id = ''
quant = {}
det = {}
items = Food_diary_new.objects.all()

z = 0
x = 0
y = 0
w = 0
for i in items:
    quant[i.food_name] = 0

# function to authenticate user


def check_user(loginID, password):
    url = "http://tpancare.panhealth.com/panwebservicev1/Service.asmx?WSDL"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data = """<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                      <soap:Body>
                        <getMemberinfo_json xmlns="http://tempuri.org/">
                          <strUserid>"""+str(loginID)+"""</strUserid>
                          <strPass>"""+str(password)+"""</strPass>
                        </getMemberinfo_json>
                      </soap:Body>
                    </soap:Envelope>"""

    response = requests.post(url, data=data, headers=headers)
    jsonobj = json.loads(response.content.decode(
        'utf-8').strip().split('<?xml')[0])
    if(jsonobj['Posts']):
        det['Firstname'] = jsonobj['Posts'][0]['ME_FIRSTNAME']
        det['Lastname'] = jsonobj['Posts'][0]['ME_LASTNAME']
        return 1
    else:
        return 0


def checker(s, z):
    if not re.search(s, z[3]):
        return 0
    else:
        return re.search(s, z[3]).group(1)

# function to get details of a particular food using food name


def get_food_details(f_name):
    url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <getFood xmlns="http://tempuri.org/">
        <name>"""+str(f_name)+"""</name>
        </getFood>
    </soap:Body>
    </soap:Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    response = requests.post(url, data=data, headers=headers)
    x = response.content.decode('utf-8')
    z = x.strip().split('Table')
    dic = {}
    dic['food_name'] = re.search('<FM_NAME>(.*)</FM_NAME>', z[3]).group(1)
    dic['ss_code'] = checker('<FM_SS_CODE>(.*)</FM_SS_CODE>', z)
    dic['fat'] = checker('<FM_FAT>(.*)</FM_FAT>', z)
    dic['fiber'] = checker('<FM_FIBER>(.*)</FM_FIBER>', z)
    dic['sugar'] = checker('<FM_SUGAR>(.*)</FM_SUGAR>', z)
    dic['sodium'] = checker('<FM_SODIUM>(.*)</FM_SODIUM>', z)
    dic['alchohol'] = checker('<FM_ALCHOHOL>(.*)</FM_ALCHOHOL>', z)
    dic['calorie'] = checker('<FM_CALORIE>(.*)</FM_CALORIE>', z)
    dic['calorie_saturated_fat'] = checker(
        '<FM_CALORIE_SATURATED_FATS>(.*)</FM_CALORIE_SATURATED_FATS>', z)
    dic['protein'] = checker('<FM_PROTIN>(.*)</FM_PROTIN>', z)
    dic['carbs'] = checker('<FM_CARBOHYDRATE>(.*)</FM_CARBOHYDRATE>', z)
    dic['f_id'] = checker('<FM_SEQID>(.*)</FM_SEQID>', z)
    dic['image_link'] = checker('<FM_IMAGEPATH>(.*)</FM_IMAGEPATH>', z)
    return dic


def checkemail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False


def home(request):
    global user_id
    if request.method == "POST":
        user = request.POST['userId']
        # checkemail(user)
        if checkemail(email=user):
            messages.error(request, "Please Enter Valid 'User ID'.")
            return redirect("/")

        pwd = request.POST['pwd']
        request.session['user'] = user
        user_id = user
        result = check_user(user, pwd)

        global w
        w = w+1
        if w == 1:
            try:
                unsav = Unsaved_new.objects.all()
                for i in unsav:
                    if(i.user_id == user):
                        entry = Temporary_new(
                            user_id=user,
                            food_name=i.food_name,
                            quantity=i.quantity,
                            mfg_code=i.mfg_code,
                            meal_type=i.meal_type,
                            ss_code=i.ss_code,
                            Food_id=i.Food_id,
                            carbs=i.carbs,
                            protein=i.protein,
                            fat=i.fat,
                            fiber=i.fiber,
                            sugar=i.sugar,
                            sodium=i.sodium,
                            alchohol=i.alchohol,
                            calorie=i.calorie,
                            calorie_saturated_fats=i.calorie_saturated_fats)
                        entry.save()
                        i.delete()
                uns = Unsaved_purchase_new.objects.all()
                for j in uns:
                    if(j.user_id == user):
                        ent = Temporary_purchase_new(
                            user_id=user,
                            mfg_code=j.mfg_code,
                            food_name=j.food_name,
                            quantity=j.quantity,
                            ss_code=j.ss_code,
                            Food_id=j.Food_id,
                            carbs=j.carbs,
                            protein=j.protein,
                            fat=j.fat,
                            fiber=j.fiber,
                            sugar=j.sugar,
                            sodium=j.sodium,
                            alchohol=j.alchohol,
                            calorie=j.calorie,
                            calorie_saturated_fats=j.calorie_saturated_fats)
                        ent.save()

                    else:
                        continue

            except Unsaved_new.DoesNotExist:
                item = None

        if result == 0:
            messages.error(request, "Invalid UserId or Password!")
            return redirect('/')
        else:
            allTypes = Main_page.objects.all()
            con = {'allTypes': allTypes}
            return render(request, 'home.html', con)
    else:

        return render(request, 'home.html')


'''def renderhome(request):
    return render(request,'home.html')'''


def details(request, f_name):

    food_det = get_food_details(f_name)
    img_url = food_det['image_link']
    img_url = img_url.replace('//', '/')
    img_url = img_url.replace('http:/pancare.', 'http://tpancare.')
    return render(request, 'details.html', {'info': food_det, 'food_name': f_name, 'image_link': img_url})


def add_item1(request):
    user = user_id
    if request.method == "POST":
        meal = request.POST["meal_type"]
        f_name = request.POST["item"]
        seq_id = request.POST["seqid"]
        qnt = request.POST["selectedQuant"]
        dic = {}
        dic = get_food_details(seq_id)
        f_id = dic['f_id']
        cal = dic['calorie']
        prot = dic['protein']
        fat = dic['fat']
        fiber = dic['fiber']
        carbs = dic['carbs']
        sat = dic['calorie_saturated_fat']
        sod = dic['sodium']
        sug = dic['sugar']
        alc = dic['alchohol']
        ss_c = dic['ss_code']
        prot = float(prot)
        fat = float(fat)
        fiber = float(fiber)
        carbs = float(carbs)
        sat = float(sat)
        sod = float(sod)
        sug = float(sug)
        alc = float(alc)
        cal = float(cal)
        num = float(qnt)
        new_entry = Temporary_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            meal_type=meal,
            ss_code=ss_c,
            Food_id=f_id,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num
        )
        new_entry.save()
        return redirect('/north')


def table(request):
    user = user_id
    try:
        item = Temporary_new.objects.filter(user_id=user)
    except Temporary_new.DoesNotExist:
        item = None

    return render(request, 'table.html', {'info': item})


def purchase(request):
    user = user_id
    try:
        item = Temporary_purchase_new.objects.filter(user_id=user)
    except Temporary_purchase_new.DoesNotExist:
        item = None

    return render(request, 'purchase.html', {'info': item})


def confirm_purchase(request):
    user = user_id
    if request.method == "POST":
        f_name = request.POST["selectedItem2"]
        qnt = request.POST["selectedQuant"]
        seq_id = request.POST["sq"]
        dic = {}
        dic = get_food_details(seq_id)
        f_id = dic['f_id']
        cal = dic['calorie']
        prot = dic['protein']
        fat = dic['fat']
        fiber = dic['fiber']
        carbs = dic['carbs']
        sat = dic['calorie_saturated_fat']
        sod = dic['sodium']
        sug = dic['sugar']
        alc = dic['alchohol']
        ss_c = dic['ss_code']
        prot = int(prot)
        fat = int(fat)
        fiber = int(fiber)
        carbs = int(carbs)
        sat = int(sat)
        sod = int(sod)
        sug = int(sug)
        alc = int(alc)
        cal = int(cal)
        num = int(qnt)
        new_entry = Temporary_purchase_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            ss_code=ss_c,
            Food_id=f_id,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num
        )

        new_entry.save()
        try:
            item = Temporary_purchase_new.objects.all()
        except Temporary_purchase_new.DoesNotExist:
            item = None

        return redirect('/north')


def confirm_purchase2(request):
    user = user_id
    if request.method == "POST":
        f_name = request.POST["selectedItem"]
        m = request.POST["mfg"]
        f_id = request.POST["fd_id"]
        cal = request.POST["cal"]
        fat = request.POST["fat"]
        prot = request.POST["protin"]
        carbs = request.POST["carbs"]
        qnt = request.POST["quantity"]
        fiber = request.POST["fiber"]
        sat = request.POST["sat"]
        sod = request.POST["sodium"]
        sug = request.POST["sugar"]
        alc = request.POST["alc"]
        ss_c = request.POST["ss_c"]

        prot = int(prot)
        fat = int(fat)
        fiber = int(fiber)
        carbs = int(carbs)
        sat = int(sat)
        sod = int(sod)
        sug = int(sug)
        alc = int(alc)
        cal = int(cal)
        num = int(qnt)
        new_entry = Temporary_purchase_new(
            user_id=user,
            food_name=f_name,
            mfg_code=m,
            quantity=qnt,
            ss_code=ss_c,
            Food_id=f_id,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num
        )

        new_entry.save()
        try:
            item = Temporary_purchase_new.objects.all()
        except Temporary_purchase_new.DoesNotExist:
            item = None

        return redirect('/purchase')


def delete(request, f_name):
    user = user_id
    instance = Temporary_new.objects.get(food_name=f_name)
    instance.delete()
    unsav = Unsaved_new.objects.all()
    tod = datetime.date(datetime.now())
    for i in unsav:
        if(i.user_id == user and i.date == tod and i.food_name == f_name):
            i.delete()
    quant[f_name] = 0
    try:
        item = Temporary_new.objects.all()
        return redirect('/table')
    except Temporary_new.DoesNotExist:
        return redirect('/home')


def delete_purchase(request, f_id):
    user = user_id
    f_id = int(f_id)
    instance = Temporary_purchase_new.objects.get(Food_id=f_id)
    instance.delete()
    unsav = Unsaved_purchase_new.objects.all()
    tod = datetime.date(datetime.now())

    for i in unsav:
        if(i.user_id == user and i.Food_id == f_id):
            i.delete()

    try:
        item = Temporary_purchase_new.objects.all()
        return redirect('/purchase')
    except Temporary_purchase_new.DoesNotExist:
        return redirect('/home')

# function to store consumption details into pancare userlog


def store_pancare(userID, f_name, date, time, meal, ss_c, qnt, cal):
    url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data2 = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
        <FoodLog xmlns="http://tempuri.org/">
        <ME_ID>"""+str(userID)+"""</ME_ID>
        <Date>"""+str(date)+"""</Date>
        <Time>"""+str(time)+"""</Time>
        <Food_Name>"""+str(f_name)+"""</Food_Name>
        <Mealtype>"""+str(meal)+"""</Mealtype>
        <Serving_Style>"""+str(ss_c)+"""</Serving_Style>
        <Food_Quntity>"""+str(qnt)+"""</Food_Quntity>
        <Food_Calorie>"""+str(cal)+"""</Food_Calorie>
        <timezone></timezone>
        </FoodLog>
    </soap:Body>
    </soap:Envelope>"""
    r = requests.post(url, data=data2, headers=headers)


def save_table(request):
    user = user_id

    try:
        item = Temporary_new.objects.all()

        for i in item:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            tod = datetime.date(datetime.now())
            store_pancare(user, i.food_name, tod, current_time,
                          i.meal_type, i.ss_code, i.quantity, i.calorie)
            entry = Transaction_det_new(
                user_id=user,
                date=tod,
                mfg_code=i.mfg_code,
                time_rec=current_time,
                food_name=i.food_name,
                quantity=i.quantity,
                meal_type=i.meal_type,
                ss_code=i.ss_code,
                Food_id=i.Food_id,
                carbs=i.carbs,
                protein=i.protein,
                fat=i.fat,
                fiber=i.fiber,
                sugar=i.sugar,
                sodium=i.sodium,
                alchohol=i.alchohol,
                calorie=i.calorie,
                calorie_saturated_fats=i.calorie_saturated_fats)

            entry.save()
            Temporary_new.objects.all().delete()
            unsav = Unsaved_new.objects.all()
            tod = datetime.date(datetime.now())
            for i in unsav:
                if(i.user_id == user and i.date == tod):
                    i.delete()
        return redirect('/home')

    except Transaction_det_new.DoesNotExist:
        return redirect('/home')


def save_purchase(request):
    user = user_id
    try:
        item = Temporary_purchase_new.objects.all()

        for i in item:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            entry = Purchase_det_new(
                user_id=user,
                date=datetime.date(datetime.now()),
                mfg_code=i.mfg_code,
                time_rec=current_time,
                food_name=i.food_name,
                quantity=i.quantity,
                ss_code=i.ss_code,
                Food_id=i.Food_id,
                carbs=i.carbs,
                protein=i.protein,
                fat=i.fat,
                fiber=i.fiber,
                sugar=i.sugar,
                sodium=i.sodium,
                alchohol=i.alchohol,
                calorie=i.calorie,
                calorie_saturated_fats=i.calorie_saturated_fats)

            entry.save()
            Temporary_purchase_new.objects.all().delete()
            unsav = Unsaved_purchase_new.objects.all()
            tod = datetime.date(datetime.now())
            for i in unsav:
                if(i.user_id == user and i.date == tod):
                    i.delete()
        return redirect('/home')

    except Transaction_det_new.DoesNotExist:
        return redirect('/home')


def deletetemp(request):
    global w
    try:
        user = user_id
        items = Temporary_new.objects.all()

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        for i in items:
            quant[i.food_name] = 0
            entry = Unsaved_new(
                user_id=user,
                date=datetime.date(datetime.now()),
                time_rec=current_time,
                food_name=i.food_name,
                quantity=i.quantity,
                meal_type=i.meal_type,
                ss_code=i.ss_code,
                Food_id=i.Food_id,
                carbs=i.carbs,
                protein=i.protein,
                fat=i.fat,
                fiber=i.fiber,
                sugar=i.sugar,
                sodium=i.sodium,
                alchohol=i.alchohol,
                calorie=i.calorie,
                calorie_saturated_fats=i.calorie_saturated_fats)

            entry.save()

        it = Temporary_purchase_new.objects.all()

        for j in it:
            entry = Unsaved_purchase_new(
                user_id=user,
                date=datetime.date(datetime.now()),
                time_rec=current_time,
                food_name=j.food_name,
                quantity=j.quantity,
                ss_code=j.ss_code,
                Food_id=j.Food_id,
                carbs=j.carbs,
                protein=j.protein,
                fat=j.fat,
                fiber=j.fiber,
                sugar=j.sugar,
                sodium=j.sodium,
                alchohol=j.alchohol,
                calorie=j.calorie,
                calorie_saturated_fats=j.calorie_saturated_fats)

            entry.save()
        w = 0
        Temporary_new.objects.all().delete()
        Temporary_purchase_new.objects.all().delete()
        return HttpResponseRedirect('/')
    except Temporary_new.DoesNotExist:
        w = 0
        return HttpResponseRedirect('/')


def profile_page(request):
    user = user_id
    name = str(det['Firstname'])+' '+str(det['Lastname'])
    return render(request, 'profile_page.html', {'name': name, 'user': user})


def userfoodlogchart(request):
    url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }

    data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
    <soapenv:Header/>
    <soapenv:Body>
        <tem:GetUserFoodLog>
            <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
            <tem:FoodName></tem:FoodName>
            <tem:fromDate></tem:fromDate>
            <tem:toDate></tem:toDate>
        </tem:GetUserFoodLog>
    </soapenv:Body> 
    </soapenv:Envelope>"""

    response = requests.post(url, data=data2, headers=headers)

    x = response.content.decode('utf-8')
    z = x.strip().split('Table')

    food_name = []
    date = []
    quantity = []
    calorie = []
    meal_type = []
    time = []

    for i in range(3, len(z)):
        if(i % 3 == 0):
            food_name.append(
                re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
            date.append(
                re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
            quantity.append(
                re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
            calorie.append(
                re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
            meal_type.append(
                re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
            time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

    user_log = pd.DataFrame()
    user_log['food_name'] = food_name
    user_log['date'] = date
    user_log['time'] = time
    user_log['quantity'] = quantity
    user_log['calorie'] = calorie
    user_log['meal_type'] = meal_type
    # print(user_log)
    today = datetime.strptime(
        str(dt.date.today()), '%Y-%m-%d').strftime('%m/%d/%Y')
    # print(today)

    pie_df = user_log[user_log.date == today]

    alldata = []
    for i in range(pie_df.shape[0]):
        temp = pie_df.iloc[i]
        alldata.append(dict(temp))
    alldata = dumps(alldata)
    # print(alldata)

    if request.method == 'POST':
        fromdate = request.POST["fromdate"]
        if fromdate == "":
            messages.warning(request, "Please Enter 'From' Date.")
            return redirect("/home/userfoodlogchart")
        else:
            fromdate = pd.to_datetime(fromdate)

        todate = request.POST["todate"]
        if todate == "":
            todate = pd.to_datetime(dt.datetime.today())
            print(todate)
        else:
            todate = pd.to_datetime(todate)

        if fromdate > todate:
            messages.warning(request, "Mismatch Of Dates!!!")
            return redirect("/home/userfoodlogchart")

        mealtype = request.POST["mealtype"]
        print(mealtype)
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type
        user_log["date"] = pd.to_datetime(user_log['date'])

        if mealtype == 'all' or mealtype == "Select":
            chart_df = user_log[((user_log.date >= fromdate)
                                 & (user_log.date <= todate))]
            dateset = sorted(set(chart_df["date"]))
            calorie_sums = []
            for i in range(len(dateset)):
                numcal = sum(pd.to_numeric(
                    chart_df[(chart_df.date == dateset[i])]['calorie']))
                calorie_sums.append(numcal)

            alldates = []
            for d in dateset:
                alldates.append(str(d.date()))

            cal_list = list(zip(alldates, calorie_sums))
            # print(cal_list)
            s = ["date", "sum"]
            mw = {"min. calories req. for men": 2000,
                  "min. calories req. for women": 1600}
            cal_data = []

            for i in range(len(alldates)):
                a = dict(zip(s, list(cal_list[i])))
                a.update(mw)
                cal_data.append(a)
            # print(cal_data)
            cal_data = dumps(cal_data)
            # print(cal_data)

            return render(request, 'userfoodlogchart.html', context={"cal_data": cal_data, "data": alldata, "fromdate":fromdate, "todate":todate})

        else:
            chart_df = user_log[((user_log.date >= fromdate) & (
                user_log.date <= todate)) & (user_log.meal_type == mealtype)]
            dateset = sorted(set(chart_df["date"]))
            # print(dateset)
            calorie_sums = []
            bfcals = []
            lunchcals = []
            snackscals = []
            dinnercals = []

            for i in range(len(dateset)):
                numcal = sum(pd.to_numeric(
                    chart_df[(chart_df.date == dateset[i])]['calorie']))
                calorie_sums.append(numcal)

            # print(calorie_sums)

            alldates = []
            for d in dateset:
                alldates.append(str(d.date()))
            # print(alldates)

            cal_list = list(zip(alldates, calorie_sums))
            # print(cal_list)
            s = ["date", "sum"]
            mw = {"min. calories req. for men": 2000,
                  "min. calories req. for women": 1600}
            cal_data = []
            for i in range(len(alldates)):
                a = dict(zip(s, list(cal_list[i])))
                a.update(mw)
                cal_data.append(a)
            # print(cal_data)
            cal_data = dumps(cal_data)
            # print(cal_data)

            return render(request, 'userfoodlogchart.html', context={"cal_data": cal_data, "data": alldata})

    return render(request, 'userfoodlogchart.html', context={"data": alldata})


def foodtopan(request):
    user = user_id
    if request.method == "POST":
        f_name = request.POST.get("selectedItem")
        desc = request.POST.get("desc")
        m = request.POST.get("mfg")
        f_id = request.POST.get("fd_id")
        cal = request.POST.get("cal")
        fat = request.POST.get("fat")
        prot = request.POST.get("protin")
        carbs = request.POST.get("carbs")
        qnt = request.POST.get("quantity")
        fiber = request.POST.get("fiber")
        sat = request.POST.get("sat")
        sod = request.POST.get("sodium")
        sug = request.POST.get("sugar")
        alc = request.POST.get("alc")
        ss_c = request.POST.get("ss_c")
        sat = request.POST.get("sat")
        meal = request.POST.get("meal_type")

        prot = float(prot)
        fat = float(fat)
        fiber = float(fiber)
        carbs = float(carbs)
        sat = float(sat)
        sod = float(sod)
        sug = float(sug)
        alc = float(alc)
        cal = float(cal)
        num = float(qnt)
        new_entry = Temporary_new(
            user_id=user,
            food_name=f_name,
            quantity=qnt,
            meal_type=meal,
            ss_code=ss_c,
            Food_id=f_id,
            carbs=carbs*num,
            protein=prot*num,
            fat=fat*num,
            fiber=fiber*num,
            sugar=sug*num,
            sodium=sod*num,
            alchohol=alc*num,
            calorie=cal*num,
            calorie_saturated_fats=sat*num
        )
        new_entry.save()
        print(carbs, fat, prot)

        url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
        headers = {"Content-Type": "text/xml; charset=utf-8"}

        data2 = """<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <AddFood xmlns="http://tempuri.org/">
            <ME_ID>"""+str(user_id)+"""</ME_ID>
            <Name>"""+str(f_name)+"""</Name>
            <Description>"""+str(desc)+"""</Description>
            <ss_code>"""+str(ss_c)+"""</ss_code>
            <Protin>"""+str(prot)+"""</Protin>
            <Carbohydrate>"""+str(carbs)+"""</Carbohydrate>
            <Fat>"""+str(fat)+"""</Fat>
            <Fiber>"""+str(fiber)+"""</Fiber>
            <Sugar>"""+str(sug)+"""</Sugar>
            <Sodium>"""+str(sod)+"""</Sodium>
            <Alchohol>"""+str(alc)+"""</Alchohol>
            <Calorie>"""+str(cal)+"""</Calorie>
            <Calorie_saturated_fats>"""+str(sat)+"""</Calorie_saturated_fats>
            </AddFood>
        </soap:Body>
        </soap:Envelope>"""
        print(data2)

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')
        print(z[0])
        if "true" in z[0]:
            messages.success(
                request, f"Food Item:{f_name} added successfully to PAN!!")
        elif "false" in z[0]:
            messages.error(request, f"Can not add food item.")

        return redirect("/home/table")


calx = []
listdate = []


def null_val(s):
    if not s:
        s = '0'
    else:
        s = s.group(1)
    return s


def chartof(request):
    if request.method == 'POST':
        if(len(calx) > 0):
            del calx[:]
        nuttype = str(request.POST['charts'])
        # datex=str(request.POST['fromdate'])
        dateobj = request.POST["fromdate"]
        nd = datetime.strptime(dateobj, '%Y-%m-%d')
        newdate = datetime.strptime(dateobj, '%Y-%m-%d').strftime('%m/%d/%Y')
        curr_date = str(newdate)
        print(newdate)

        url = "http://tpancare.panhealth.com/PickPillversion1/pickpillservice.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body>
        </soapenv:Envelope>"""
        resp = requests.post(url, data=data2, headers=headers)
        x = resp.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        for i in range(0, len(calorie)):
            calorie[i] = int(calorie[i])
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type

       
        prev_date = dt.date.today() - dt.timedelta(days=1)
        d4 = dt.date.strftime(prev_date, "%m/%d/%Y")
        
        if(len(calx) > 0):
            del calx[:]

        for i in range(5):
            prev_date = nd - dt.timedelta(days=i)
            d4 = dt.date.strftime(prev_date, "%m/%d/%Y")
            # print(d4)

            listdate.append(d4)
        # print(listdate)
        listof = []
        cal = ''
        calex = ''
        if(nuttype == 'calorie'):
            cal = '<FM_CALORIE>'
            calex = '</FM_CALORIE>'
        elif(nuttype == 'carbohydrate'):
            cal = '<FM_CARBOHYDRATE>'
            calex = '</FM_CARBOHYDRATE>'
        elif(nuttype == 'sodium'):
            cal = '<FM_SODIUM>'
            calex = '</FM_SODIUM>'
        elif(nuttype == 'sugar'):
            cal = '<FM_SUGAR>'
            calex = '</FM_SUGAR>'
        elif(nuttype == 'alcohol'):
            cal = '<FM_ALCHOHOL>'
            calex = '</FM_ALCHOHOL>'
        elif(nuttype == 'fiber'):
            cal = '<FM_FIBER>'
            calex = '</FM_FIBER>'
        else:
            cal = '<FM_FAT>'
            calex = '</FM_FAT>'

        nutdata = []

        for i in user_log['food_name']:
            strin = i
            # print(strin)
            data = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <getFood xmlns="http://tempuri.org/">
                    <name>"""+str(strin)+"""</name>
                    </getFood>
                </soap:Body>
                </soap:Envelope>"""
            r = requests.post(url, data=data, headers=headers)
            response = requests.post(url, data=data, headers=headers)
            x = response.content.decode('utf-8')
            z = x.strip().split('Table')
            ss = re.search(cal+'(.*)'+calex, z[3])
            nutdata.append(null_val(ss))

        for i in range(0, len(nutdata)):
            nutdata[i] = float(nutdata[i])*int(user_log['quantity'][i])
            # print(nutdata[i])
        user_log['nutdata'] = nutdata
        for i in listdate:
            dfxx = user_log[user_log['date'] == i]
            cali = np.sum(dfxx['nutdata'])
            calx.append(cali)
        fromdate=listdate[-1]
        todate=listdate[-5]
        cont = {'nuttype': nuttype , 'fromdate':fromdate , 'todate':todate}
        return render(request, 'index.html', cont)
    else:
        return render(request, 'index.html')


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        labels = listdate[-5:]
        chartLabel = "Total Nutrition per day"
        chartdata = calx[-5:]
        data = {
            "labels": labels,
            "chartLabel": chartLabel,
            "chartdata": chartdata,
        }

        return Response(data)


def purchase_status(request):
    all_objects = Purchase_det_new.objects.all().values()
    all_obj = Purchase_det_new.objects.all()
    df = pd.DataFrame(all_objects)

    dfz = df[df['user_id'] == user_id]
    dfz.drop('Food_id', inplace=True, axis='columns')
    dfz.drop('food_type', inplace=True, axis='columns')
    dfz.drop('calorie_saturated_fats', inplace=True, axis='columns')
    dfz.drop('ss_code', inplace=True, axis='columns')
    dfz.drop('alchohol', inplace=True, axis='columns')
    dfz.drop('sodium', inplace=True, axis='columns')
    dfz.drop('user_id', inplace=True, axis='columns')
    #print(dfz)

    con = {'all_objects': all_objects, 'all_obj': all_obj, 'dfz': dfz}
    return render(request, 'purchase_status.html', con)


def purchasechart(request):
    if request.method == 'POST':
        all_objects = Purchase_det_new.objects.all().values()
        all_obj = Purchase_det_new.objects.all()
        df = pd.DataFrame(all_objects)
        dfz = df[df['user_id'] == user_id]

        def func(date):
            return datetime.strftime(date, '%Y-%m-%d')

        def func2(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        dfz['date'] = dfz['date'].apply(func)
        #print(dfz['date'])
        purchaseset = list(set(list(dfz["food_name"])))
        #print(dfz)
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type
        print(user_log)
        consumeset = list(set(list(user_log["food_name"])))
        #print(consumeset)
        #print(purchaseset)
        fromdate = request.POST["fromdate"]
        #frmjson = []
        
        todate = request.POST["todate"]
        #tojson = []

        datevals = [{"fromd":fromdate}, {"tod":todate}]
        
        newdate1 = datetime.strptime(fromdate, '%Y-%m-%d').strftime('%m/%d/%Y')
        newdate2 = datetime.strptime(todate, '%Y-%m-%d').strftime('%m/%d/%Y')

        if newdate1 > newdate2:
            messages.warning(request, "Mismatch Of Dates!!!")
            return redirect("/home/purchasechart")
        
        food_quantity = ["food_name", "quantity"]
        
        purchasedata = []
        pdata = []
        for i in purchaseset:
            dfz2 = dfz[((dfz.date >= fromdate) & (dfz.date <= todate)) & (dfz.food_name == i)]
            sums = sum(list(map(int, list(dfz2["quantity"]))))
            pdata.append([i, sums])
        for i in range(len(pdata)):
            purchasedata.append(dict(zip(food_quantity, pdata[i])))
        purchasedata = dumps(purchasedata)
        print(purchasedata)

        consumedata = []
        cdata = []
        for i in consumeset:
            consumedf = user_log[(user_log.date <= newdate2) & (user_log.date >= newdate1)]
            consumedf =   consumedf[(user_log.food_name == i)]
            #print(consumedf["food_name"], consumedf["quantity"])
            sums = sum(list(map(int, list(consumedf["quantity"]))))
            cdata.append([i, sums])
        for i in range(len(cdata)):
            consumedata.append(dict(zip(food_quantity, cdata[i])))
        consumedata = dumps(consumedata)
        print(consumedata)

        return render(request, 'purchasechart.html', context={"consumedata": consumedata, "purchasedata": purchasedata, "fromdate":fromdate, "todate":todate})
    else:
        return render(request, "purchasechart.html")


def otherdayanalysis(request):
    if request.method == 'POST':
        url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8"
        }
        dateobj = request.POST["dateinput2"]
        if dateobj == '':
            messages.warning(request, "Please Enter Date.")
            return redirect("/home/userdate_form")
        newdate = datetime.strptime(dateobj, '%Y-%m-%d').strftime('%m/%d/%Y')
        newdate = str(newdate)
        mealtype = request.POST["mealtype2"]

        data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
        <soapenv:Header/>
        <soapenv:Body>
            <tem:GetUserFoodLog>
                <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
                <tem:FoodName></tem:FoodName>
                <tem:fromDate></tem:fromDate>
                <tem:toDate></tem:toDate>
            </tem:GetUserFoodLog>
        </soapenv:Body> 
        </soapenv:Envelope>"""

        response = requests.post(url, data=data2, headers=headers)

        x = response.content.decode('utf-8')
        z = x.strip().split('Table')

        food_name = []
        date = []
        quantity = []
        calorie = []
        meal_type = []
        time = []

        for i in range(3, len(z)):
            if(i % 3 == 0):
                food_name.append(
                    re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
                date.append(
                    re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
                quantity.append(
                    re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
                calorie.append(
                    re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
                meal_type.append(
                    re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
                time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))

        user_log = pd.DataFrame()
        user_log['food_name'] = food_name
        user_log['date'] = date
        user_log['time'] = time
        user_log['quantity'] = quantity
        user_log['calorie'] = calorie
        user_log['meal_type'] = meal_type

        dateset = sorted(set(user_log['date']))
        if mealtype != "all" and mealtype != "Select":
            chart_df = user_log[(user_log.date == newdate)
                                & (user_log.meal_type == mealtype)]
            alldata = []
            #caloriesum = pd.to_numeric(chart_df["calorie"]).sum()
            for i in range(chart_df.shape[0]):
                temp = chart_df.iloc[i]
                alldata.append(dict(temp))
            alldata = dumps(alldata)

            return render(request, 'userdate_form.html', context={"alldata": alldata})

        else:
            chart_df = user_log[(user_log.date == newdate)]
            alldata = []

            for i in range(chart_df.shape[0]):
                temp = chart_df.iloc[i]
                alldata.append(dict(temp))
            alldata = dumps(alldata)
            context = {"data": alldata}

            return render(request, 'userdate_form.html', context={"alldata": alldata})
    else:
        return render(request, 'userdate_form.html')


def consumer_history(request):
    url = "http://tpancare.panhealth.com/DietDiaryService/DietDiaryService.asmx?WSDL"
    headers = {
        "Content-Type": "text/xml; charset=utf-8"
    }
    data2 = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetUserFoodLog>
         <tem:ME_ID>"""+str(user_id)+"""</tem:ME_ID>
         <tem:FoodName></tem:FoodName>
         <tem:fromDate></tem:fromDate>
         <tem:toDate></tem:toDate>
      </tem:GetUserFoodLog>
   </soapenv:Body>
    </soapenv:Envelope>"""
    response = requests.post(url, data=data2, headers=headers)

    x = response.content.decode('utf-8')
    z = x.strip().split('Table')
    food_name = []
    date = []
    quantity = []
    calorie = []
    meal_type = []
    time = []

    for i in range(3, len(z)):
        if(i % 3 == 0):
            # print(z[i])
            # print("\n")
            food_name.append(
                re.search('<FOODNAME>(.*)</FOODNAME>', z[i]).group(1))
            date.append(re.search('<FOODDATE>(.*)</FOODDATE>', z[i]).group(1))
            quantity.append(
                re.search('<FOOD_QUNTITY>(.*)</FOOD_QUNTITY>', z[i]).group(1))
            calorie.append(re.search('<CALORIE>(.*)</CALORIE>', z[i]).group(1))
            meal_type.append(
                re.search('<MEALTYPE>(.*)</MEALTYPE>', z[i]).group(1))
            time.append(re.search('<TIME>(.*)</TIME>', z[i]).group(1))
    user_log = pd.DataFrame()
    user_log['food_name'] = food_name
    user_log['date'] = date
    user_log['time'] = time
    user_log['quantity'] = quantity
    user_log['calorie'] = calorie
    user_log['meal_type'] = meal_type
    user_log = user_log.sort_values('date', ascending=False)
    print(user_log)

    con = {'user_log': user_log}
    return render(request, 'consumer_history.html', con)
