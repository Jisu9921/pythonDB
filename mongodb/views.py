from django.http import HttpResponse
from django.shortcuts import render
from pymongo import MongoClient
import json


def mongo_index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        client_mongo = MongoClient('localhost', 27017)
        mongo_db = client_mongo.pymongo
        user = mongo_db.user
        user_info = {"name": name}
        user.insert_one(user_info).inserted_id
        result = dict(msg=1)
        return HttpResponse(json.dumps(result), content_type="application/json")
    return render(request, 'view/mongo.html')

