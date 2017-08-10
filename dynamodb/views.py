from django.http import HttpResponse
import boto3
import json
dynamodb = boto3.resource('dynamodb')


def create_table_dynamon(request):
    table = dynamodb.create_table(
        TableName='schedule',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName='schedule')
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def insert_schedule_dynamo(request):
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_schedule_dynamo(request):
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def delete_schedule_dynamo(request):
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")