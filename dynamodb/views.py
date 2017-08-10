from django.http import HttpResponse
from django.shortcuts import render
import boto3
import json


def dynamo_index(request):
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')
    table.delete_item(
        Key={
            'username': 'janedoe',
            'last_name': 'Doe'
        }
    )
    print(table.item_count)
    return render(request, 'view/dynamo.html')
