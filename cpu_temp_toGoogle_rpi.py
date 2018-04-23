#!/usr/bin/env python3

'''
service account from raspberries.sirrisdiepenbeek2@gmail.com
sending through google-api-python-client
to spreadsheet in google drive from abovementioned google account.
'''

import os
import sys
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

# reading from a spreadsheet just to see whether communication works
result = service.spreadsheets().values().get(
    spreadsheetId=spreadsheetID,
    range='b1:b3').execute()
print(result)

def add_row_to_google_sheet():
    # request to add one Row at the end of the spreadsheet
    requests = [{
        "appendDimension": {
            "sheetId": 0,
            "dimension": "ROWS",
            "length": 1}}]
    body = {"requests": requests}
    response = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetID, body=body).execute()

def add_variable_to_google_sheet(values):
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetID, valueInputOption='RAW', range='a2:b2', body=values).execute()

def create_sine_variable():
    sine_variables=[]
    for x in range(0, 359):
        weight = math.sin(math.radians(x))*100  # create sine shaped variable in time
        sine_variables.append(weight)
    return sine_variables

# service.spreadsheets().sheets().copyTo(spreadsheetId='1BiuNIMDZ3hCJxhVDoHtK-HbSXcYHDBVPMxNxIfF_qyE')
# service.spreadsheets().sheets().duplicateActiveSheet()

def get_cpu_temperature():
    # Return CPU temperature as a character string
    res = os.popen('vcgencmd measure_temp').readline()
    return(float(res.replace("temp=","").replace("'C\n","")))

def main():
    while 1:
        #create sine variable
        # result=create_sine_variable()
        # for i in range (0, len(result)):
        #     this_value = result[i]
        #     this_time = time.strftime('%m/%d/%Y %H:%M:%S')
        #     this_value_pair = [[this_time, this_value]]
        #     add_row_to_google_sheet()
        #     values = {'values': this_value_pair}
        #     add_variable_to_google_sheet(values)
        #     print(values)
        #     time.sleep(5)

        this_value = get_cpu_temperature()
        this_time = time.strftime('%d/%m/%Y %H:%M:%S')
        this_value_pair = [[this_time, "", this_value]]
        add_row_to_google_sheet()
        values = {'values': this_value_pair}
        add_variable_to_google_sheet(values)
        print(values)
        time.sleep(60)


if __name__ == "__main__":
    main()
    sys.exit(0)
