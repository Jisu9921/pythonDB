from django.http import HttpResponse
from django.shortcuts import render
import pymysql.cursors
import json


def mysql_index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        connection_mysql = pymysql.connect(host='localhost',
                                           user='root',
                                           password='1234',
                                           db='pymysql',
                                           charset='utf8mb4',
                                           cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection_mysql.cursor() as cursor:
                sql = "INSERT INTO `users` (`name`) VALUES (%s)"
                cursor.execute(sql, (name,))
            connection_mysql.commit()
        finally:
            connection_mysql.close()
        result = dict(msg=1)
        return HttpResponse(json.dumps(result), content_type="application/json")
    return render(request, 'view/mysql.html')