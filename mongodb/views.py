from django.http import HttpResponse
from django.shortcuts import render
from scheduler.spreadsheets import *
from pymongo import MongoClient
import json
client_mongo = MongoClient('localhost', 27017)
mongo_db = client_mongo.pymongo


def insert_schedule_mongo(request):
    schedule = mongo_db.schedule
    sheet_schedules = analysis_sheet(spreadsheetId='1qEtfTDg0jn72MLDhmrUxFpJD7tzFyq-5qTySGvghKqg', channel='tvN')
    for data in sheet_schedules:
        schedule_info = {
            "channel": data['Channel'],
            "program_title": data['ProgramTitle'],
            "start_time": data['StartTime'],
            "end_time": data['EndTime']
        }
        schedule.insert_one(schedule_info)
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_schedule_mongo(request):
    schedule = mongo_db.schedule
    for data in schedule.find():
        print(data)
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def delete_schedule_mongo(request):
    schedule = mongo_db.schedule
    schedule.delete_many({})
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")
