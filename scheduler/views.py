from django.shortcuts import render
from dynamodb.views import *
from mongodb.views import *
from mysqldb.views import *
from .spreadsheets import *
import time
import json


def scheduler_index(request):
    return render(request, 'view/index.html')


def insert_schedule(request):
    sheet_schedules = analysis_sheet(spreadsheetId='1qEtfTDg0jn72MLDhmrUxFpJD7tzFyq-5qTySGvghKqg', channel='tvN')
    times = []
    dynamo_start_time = time.time()
    insert_dynamo(sheet_schedules=sheet_schedules)
    dynamo_end_time = time.time() - dynamo_start_time
    dynamo_time = ('%.04f' % (dynamo_end_time))
    times.append(dynamo_time)

    mongo_start_time = time.time()
    insert_mongo(sheet_schedules=sheet_schedules)
    mongo_end_time = time.time() - mongo_start_time
    mongo_time = ('%.04f' % (mongo_end_time))
    times.append(mongo_time)

    mysql_start_time = time.time()
    insert_mysql(sheet_schedules=sheet_schedules)
    mysql_end_time = time.time() - mysql_start_time
    mysql_time = ('%.04f' % (mysql_end_time))
    times.append(mysql_time)

    result = dict(dynamo_time=dynamo_time, mongo_time=mongo_time, mysql_time=mysql_time, max_time=max(times))
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_schedule(request):
    times = []

    dynamo_start_time = time.time()
    get_dynamo()
    dynamo_end_time = time.time() - dynamo_start_time
    dynamo_time = ('%.04f' % (dynamo_end_time))
    times.append(dynamo_time)

    mongo_start_time = time.time()
    get_mongo()
    mongo_end_time = time.time() - mongo_start_time
    mongo_time = ('%.04f' % (mongo_end_time))
    times.append(mongo_time)

    mysql_start_time = time.time()
    get_mysql()
    mysql_end_time = time.time() - mysql_start_time
    mysql_time = ('%.04f' % (mysql_end_time))
    times.append(mysql_time)

    result = dict(dynamo_time=dynamo_time, mongo_time=mongo_time, mysql_time=mysql_time, max_time=max(times))
    return HttpResponse(json.dumps(result), content_type="application/json")


def delete_schedule(request):
    times=[]

    dynamo_start_time = time.time()
    delete_dynamo()
    dynamo_end_time = time.time() - dynamo_start_time
    dynamo_time = ('%.04f' % (dynamo_end_time))
    times.append(dynamo_time)

    mongo_start_time = time.time()
    delete_mongo()
    mongo_end_time = time.time() - mongo_start_time
    mongo_time = ('%.04f' % (mongo_end_time))
    times.append(mongo_time)

    mysql_start_time = time.time()
    delete_mysql()
    mysql_end_time = time.time() - mysql_start_time
    mysql_time = ('%.04f' % (mysql_end_time))
    times.append(mysql_time)

    result = dict(dynamo_time=dynamo_time, mongo_time=mongo_time, mysql_time=mysql_time, max_time=max(times))
    return HttpResponse(json.dumps(result), content_type="application/json")
