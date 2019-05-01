#!/usr/bin/env python3

''' 
service account from raspberries.sirrisdiepenbeek2@gmail.com
sending through google-api-python-client
to spreadsheet in google drive from abovementioned google account.
''' 

import math 
import time 
from oauth2client.service_account import ServiceAccountCredentials 
from httplib2 import Http 
from googleapiclient.discovery import build

scopes = ['https://spreadsheets.google.com/feeds'] 
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/jan/klima2_Grpi_secret.json', scopes=scopes) 
spreadsheetID = '1fJ5-2CCK3b5yTaENa4srdhkgqqIhx8pj9psYG9SijFo' 
http_auth = credentials.authorize(Http()) 
service = build('sheets', 'v4', http=http_auth)

while 1:
    for x in range(0, 359):
        # request to add one Row at the end of the spreadsheet
        requests = [{
            "appendDimension": {
                "sheetId": 0,
                "dimension": "ROWS",
                "length": 1}}]
        body = {"requests": requests}
        response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=body).execute()

        # send variable to first free row in spreadsheet
        weight = math.sin(math.radians(x))*100 # create sine shaped variable in time
        this_time = time.strftime('%m/%d/%Y %H:%M:%S')
        values = {'values': [[this_time, weight]]}
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheetID, valueInputOption='RAW', range='a2:b2', body=values).execute()
        print(values)

        time.sleep(60)

# service.spreadsheets().sheets().copyTo(spreadsheetId='1BiuNIMDZ3hCJxhVDoHtK-HbSXcYHDBVPMxNxIfF_qyE') 
# service.spreadsheets().sheets().duplicateActiveSheet()
