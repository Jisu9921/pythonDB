from django.http import HttpResponse
from scheduler.spreadsheets import *
import pymysql.cursors
import json


def insert_schedule_mysql(request):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pymysql', charset='utf8mb4')
    cur = conn.cursor()
    schedule = analysis_sheet(spreadsheetId='1qEtfTDg0jn72MLDhmrUxFpJD7tzFyq-5qTySGvghKqg', channel='tvN')
    for data in schedule:
        sql = "INSERT INTO `schedule` (`channel`, `program_title`, `start_time`, `end_time`) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (data['Channel'], data['ProgramTitle'], data['StartTime'], data['EndTime'],))
    conn.commit()
    cur.close()
    conn.close()
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_schedule_mysql(request):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pymysql', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("SELECT * FROM schedule")
    cur.close()
    conn.close()
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def delete_schedule_mysql(request):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pymysql', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("DELETE FROM schedule")
    conn.commit()
    cur.close()
    conn.close()
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def insert_mysql(sheet_schedules):
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pymysql', charset='utf8mb4')
    cur = conn.cursor()
    for data in sheet_schedules:
        sql = "INSERT INTO `schedule` (`channel`, `program_title`, `start_time`, `end_time`) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (data['Channel'], data['ProgramTitle'], data['StartTime'], data['EndTime'],))
    conn.commit()
    cur.close()
    conn.close()


def get_mysql():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pymysql', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("SELECT * FROM schedule")
    cur.close()
    conn.close()


def delete_mysql():
    conn = pymysql.connect(host='localhost', user='root', password='1234', db='pymysql', charset='utf8mb4')
    cur = conn.cursor()
    cur.execute("DELETE FROM schedule")
    conn.commit()
    cur.close()
    conn.close()
