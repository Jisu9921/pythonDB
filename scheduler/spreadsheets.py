# -*- coding: utf-8 -*-

import httplib2
import os
from datetime import datetime, date
from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/drive'
APPLICATION_NAME = 'EPGAutomator'
ADVERTISEMENT_ID = '0BymTJ-LJrMywdzhLdkN3X2tOYmc'

discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
flags = tools.argparser.parse_args([])

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR_NAME = os.path.dirname(PROJECT_DIR)
CLIENT_SECRET_FILE = '{}{}'.format(PROJECT_DIR_NAME, '/client_secret.json')


def get_credentials():
    credential_dir = os.path.join(PROJECT_DIR_NAME, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'googleapis.com-python-epgautomator-drive.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def analysis_sheet(spreadsheetId, channel, sheet_name=None):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    category_row = get_sheet_category_row(spreadsheetId)
    range_column = 'A{}:Z{}'.format(category_row, category_row + 1)
    sheet_range_column = '{}!{}'.format(channel, range_column)
    sheet_range = '{}!{}'.format(channel, 'A{}:Z'.format(category_row))
    day_list = ['월', '화', '수', '목', '금', '토', '일']

    try:
        result_column = service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                            range=sheet_range_column).execute()
        result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                     range=sheet_range).execute()
    except HttpError:
        text = '시트의 {} 채널이 존재하지 않습니다'.format(channel)
        return None
    values_column = result_column.get('values', [])
    column = dict()
    if not values_column:
        return
    else:
        for row in values_column:
            for i, data in enumerate(row):
                if data == 'ProgramTitle':
                    column['ProgramTitle'] = i
                elif data == 'StartTime':
                    column['StartTime'] = i
                elif data == 'EndTime':
                    column['EndTime'] = i
                elif data == 'Type':
                    column['Type'] = i
                elif data.strip() == 'Insertion':
                    column['Insertion'] = i
                elif data == 'Date':
                    column['Date'] = i
                elif data == 'DayOfWeek':
                    column['DayOfWeek'] = i
                elif data == 'Time':
                    column['Time'] = i
                elif data == 'Day':
                    column['Day'] = i
    values = result.get('values', [])
    schedule = []
    key_error_str = ''
    if not values:
        return
    else:
        for i, row in enumerate(values):
            if i > 0:
                try:
                    if row[column['ProgramTitle']] == '':
                        program_title = schedule[-1]['ProgramTitle']
                    else:
                        program_title = row[column['ProgramTitle']]
                    try:
                        if "~" in row[column['Time']]:
                            time_split = row[column['Time']].split('~')
                        elif "-" in row[column['Time']]:
                            time_split = row[column['Time']].split('-')
                        start_time = time_split[0].strip()
                        end_time = time_split[1].strip()
                    except KeyError:
                        start_time = row[column['StartTime']]
                        end_time = row[column['EndTime']]

                    if ":" not in start_time:
                        start_time = start_time[0:2] + ":" + start_time[2:4]
                    if ":" not in end_time:
                        end_time = end_time[0:2] + ":" + end_time[2:4]
                    day_of_weeks = []
                    try:
                        for j in range(0, 7):
                            if row[int(column['Day'] + j)] != '':
                                day_of_weeks.append(dict(day=day_list[j], insertion=row[int(column['Day']) + j]))
                    except KeyError:
                        for c in row[column['DayOfWeek']]:
                            insertion = int(row[column['Insertion']].strip()) / len(row[column['DayOfWeek']])
                            day_of_weeks.append(dict(day=c.strip(), insertion=insertion))

                    schedule.append(
                        dict(ProgramTitle=program_title.strip(),
                             StartTime=start_time.strip(),
                             EndTime=end_time.strip(),
                             Type=row[column['Type']].strip(),
                             Date=row[column['Date']].split('(')[0].strip(),
                             DayOfWeek=day_of_weeks,
                             location=i + 7)
                    )

                except IndexError:
                    pass
                except KeyError:
                    key_error_str = 'ProgramTite , Time , StartTime, EndTime 등의 컬럼값을 확인해 주세요.'
    new_schedule = []
    insertion_err_list = []
    for data in schedule:
        if "~" not in data['Date']:
            try:
                date = data['Date'].split('/')[1]
                month = data['Date'].split('/')[0]
            except IndexError:
                month = ''
                date = data['Date']
            date_list = date.split(',')
            day_of_insertion = 0
            for day_of_week in data['DayOfWeek']:
                day_of_insertion += int(day_of_week['insertion'])
            if day_of_insertion != len(date_list):
                insertion_err_list.append(data['location'])
            for item in date_list:
                if len(item.strip()) > 3:
                    if '.' not in item:
                        result_month = item[0:2]
                        result_day = item[2:4]
                    else:
                        item_split = item.split('.')
                        result_month = item_split[0]
                        result_day = item_split[1]
                    try:
                        new_schedule.append(dict(
                            Channel=channel,
                            ProgramTitle=data['ProgramTitle'],
                            StartTime='2017-{}-{} {}:00'.format('{:02d}'.format(int(result_month)),
                                                                '{:02d}'.format(int(result_day)),
                                                                data['StartTime']),
                            EndTime='2017-{}-{} {}:00'.format('{:02d}'.format(int(result_month)),
                                                              '{:02d}'.format(int(result_day)),
                                                              data['EndTime']),
                            Type=data['Type']))
                    except ValueError:
                        pass
                else:
                    new_schedule.append(dict(
                        Channel=channel,
                        ProgramTitle=data['ProgramTitle'],
                        StartTime='2017-{}-{} {}:00'.format('{:02d}'.format(int(month)),
                                                            '{:02d}'.format(int(item)),
                                                            data['StartTime']),
                        EndTime='2017-{}-{} {}:00'.format('{:02d}'.format(int(month)),
                                                          '{:02d}'.format(int(item)),
                                                          data['EndTime']),
                        Type=data['Type']))
        else:
            date = data['Date'].split('~')
            start_date = date[0].split('/')[1]
            end_date = date[1].split('/')[1]
            for item in range(int(start_date), int(end_date) + 1):
                day = datetime(2017, 7, item).weekday()
                for day_of_week in data['DayOfWeek']:
                    if day_of_week['day'] == day_list[day]:
                        new_schedule.append(dict(
                            Channel=channel,
                            ProgramTitle=data['ProgramTitle'],
                            StartTime='2017-07-{} {}:00'.format('{:02d}'.format(int(item)), data['StartTime']),
                            EndTime='2017-07-{} {}:00'.format('{:02d}'.format(int(item)), data['EndTime']),
                            Type=data['Type']))
    if len(new_schedule) is 0:
        text = '{} 시트 {} 채널의 Date 를 확인해 주세요.'.format(sheet_name,channel)
    if len(insertion_err_list) is not 0:
        err_list = ''
        for i, data in enumerate(insertion_err_list):
            if i == 0:
                err_list += str(data)
            else:
                err_list += ', ' + str(data)
        text = '{}/{} 채널 {} 행의 Insertion 과 Date 의 크기가 서로 다릅니다'.format(sheet_name, channel, err_list)

    return new_schedule


def get_sheet_name(spreadsheetId):
    credentials = get_credentials()
    service = discovery.build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    values = result.get('sheets', [])
    channels = []
    if not values:
        return
    else:
        for data in values:
            if data['properties']['title'] == 'TV Summary' or data['properties']['title'] == 'TerrTV':
                pass
            else:
                channels.append(data['properties']['title'].strip())
    return channels


def get_sheet_category_row(spreadsheetId):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    range = '{}!{}'.format('tvN', 'A:Z')
    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId,
                                                 range=range).execute()
    values = result.get('values', [])
    for i, row in enumerate(values):
        for j, data in enumerate(row):
            if data == 'ProgramTitle':
                return i + 1


def convert_cue_to_epg(spreadsheetId, channel):
    credentials = get_credentials()
    spreadsheet_id = '14zZx48sjbD96j5WlZYxo36F0ceauHmahQ-JnQv07VZQ'
    service_write = discovery.build('sheets', 'v4', credentials=credentials)
    sheet_range = '{}!{}'.format('Sheet1', 'A2:E')
    request_body = {

    }
    service_write.spreadsheets().values().clear(spreadsheetId=spreadsheet_id,
                                                range=sheet_range,
                                                body=request_body).execute()
    update_data = []
    schedule = analysis_sheet(spreadsheetId, channel)
    for row in schedule:
        update_data.append([row['Channel'],
                            row['ProgramTitle'],
                            str(row['StartTime']),
                            str(row['EndTime']).split('+')[0],
                            row['Type']
                            ])
    body = {
        'value_input_option': 'RAW',
        'data': [
            {
                'values': update_data,
                'range': sheet_range
            }
        ],
    }
    service_write.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id,
                                                      body=body).execute()
    return None
