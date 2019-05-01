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
import subprocess

#GOOGLE OFF:  =  commented lines because Google api not working
#GOOGLE OFF: from oauth2client.service_account import ServiceAccountCredentials
#GOOGLE OFF: from httplib2 import Http
#GOOGLE OFF: from googleapiclient.discovery import build

from ISStreamer.Streamer import Streamer


scopes = ['https://spreadsheets.google.com/feeds']
#GOOGLE OFF: credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/jan/klima2_Grpi_secret.json', scopes=scopes)
spreadsheetID = '1fJ5-2CCK3b5yTaENa4srdhkgqqIhx8pj9psYG9SijFo'
#GOOGLE OFF: http_auth = credentials.authorize(Http())
#GOOGLE OFF: service = build('sheets', 'v4', http=http_auth)
sensor_snr = '28-051692d95eff'

# reading from a spreadsheet just to see whether communication works
#GOOGLE OFF: result = service.spreadsheets().values().get(
#GOOGLE OFF:     spreadsheetId=spreadsheetID,
#GOOGLE OFF:     range='b1:b3').execute()
#print(result)

def send_to_InitialState(temp):
    streamer = Streamer(bucket_name="Google Sheet testing", bucket_key="SheetTest", access_key="nWHNn1mOEia5I98FopFAiArcE0ZHMcKW")
    streamer.log("T_klima2", temp)
    streamer.flush()
    streamer.close()

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

def fileexists(filename):
        try:
                with open(filename): pass
        except IOError:
                return False
        return True

def get_sensor_temperature():
        #Routine to read the temperature
        #Read the sensor 10 times checking the CRC until we have a good read
        for retries in range(0, 10):
                subprocess.call(['modprobe', 'w1-gpio'])
                subprocess.call(['modprobe', 'w1-therm'])

                # Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as bef$
                filename = "/sys/bus/w1/devices/"+sensor_snr+"/w1_slave"
                if (fileexists(filename)):
                        tfile = open(filename)
                else:
                        return 0
                # Read all of the text in the file.
                text = tfile.read()
                # Close the file now that the text has been read.
                tfile.close()
                #Perform a CRC Check
                firstline  = text.split("\n")[0]
                crc_check = text.split("crc=")[1]
                crc_check = crc_check.split(" ")[1]
                if crc_check.find("YES")>=0:
                        break
        #If after 10 tries we were unable to get a good read return 0
        if retries==9:
                return(0)
        # Split the text with new lines (\n) and select the second line.
        secondline = text.split("\n")[1]
        # Split the line into words, referring to the spaces, and select the 10th word (counting from 0).
        temperaturedata = secondline.split(" ")[9]
        # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
        temperature = float(temperaturedata[2:])
        # Put the decimal point in the right place and display it.
        temperature = temperature / 1000
        temp = float(temperature)
        return(temp)


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

        this_value = get_sensor_temperature()
        this_time = time.strftime('%d/%m/%Y %H:%M:%S')
        this_value_pair = [[this_time, this_value]]
#GOOGLE OFF:  add_row_to_google_sheet()
        values = {'values': this_value_pair}
#GOOGLE OFF:         add_variable_to_google_sheet(values)
#GOOGLE OFF:         print(values)
        send_to_InitialState(this_value)
        time.sleep(10)


if __name__ == "__main__":
    main()
    sys.exit(0)
