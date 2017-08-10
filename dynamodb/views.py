from django.http import HttpResponse
from scheduler.spreadsheets import *
import boto3
import botocore
import json
import uuid
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
                'AttributeType': 'S'
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
    table = dynamodb.Table('schedule')
    sheet_schedules = analysis_sheet(spreadsheetId='1qEtfTDg0jn72MLDhmrUxFpJD7tzFyq-5qTySGvghKqg', channel='tvN')
    for data in sheet_schedules:
        table.put_item(
            Item={
                'id': str(uuid.uuid4()),
                'chaneel': data['Channel'],
                'program_title': data['ProgramTitle'],
                'start_time': data['StartTime'],
                'end_time': data['EndTime']
            }
        )
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def batch_insert_schedule_dynamo(request):
    table = dynamodb.Table('schedule')
    sheet_schedules = analysis_sheet(spreadsheetId='1qEtfTDg0jn72MLDhmrUxFpJD7tzFyq-5qTySGvghKqg', channel='tvN')
    with table.batch_writer() as batch:
        for data in sheet_schedules:
            batch.put_item(
                Item={
                    'id': str(uuid.uuid4()),
                    'chaneel': data['Channel'],
                    'program_title': data['ProgramTitle'],
                    'start_time': data['StartTime'],
                    'end_time': data['EndTime']
                }
            )
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_schedule_dynamo(request):
    table = dynamodb.Table('schedule')
    schedule = table.scan()['Items']
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")


def delete_schedule_dynamo(request):
    table = dynamodb.Table('schedule')
    schedule = table.scan()['Items']
    for data in schedule:
        table.delete_item(
            Key={
                'id': data['id']
            }
        )
    result = dict(msg=1)
    return HttpResponse(json.dumps(result), content_type="application/json")