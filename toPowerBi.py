#!/usr/bin/env python3

'''
sending temperature sensor data from myraspi to Microsoft PowerBi account jan.kempeneers@sirris.be
'''

import os, sys, math, time, subprocess, socket, urllib, urllib2
from datetime import datetime

sensor1_snr = "28-0416939b61ff" 
sensor2_snr = "28-051692afcaff"
interval = 10

# REST API endpoint, given to you when you create an API streaming dataset
# Will be of the format: https://api.powerbi.com/beta/<tenant id>/datasets/< dataset id>/rows?key=<key id>
#REST_API_URL = "https://api.powerbi.com/beta/d4c1d712-e8c2-4fdf-abce-18805891b5b0/datasets/93274b13-7094-4dd1-95f9-3273bb79422c/rows?key=BX1pWttOR8gzxTdbQSP8IVKJnUsM7p2%2Bg08SQujF8m3FZi9%2FlOUZ79OFKnmm4Yiumt1oTL6AFSuSAgxFu56Wmg%3D%3D"
REST_API_URL = "https://api.powerbi.com/beta/d4c1d712-e8c2-4fdf-abce-18805891b5b0/datasets/93274b13-7094-4dd1-95f9-3273bb79422c/rows?key=BX1pWttOR8gzxTdbQSP8IVKJnUsM7p2%2Bg08SQujF8m3FZi9%2FlOUZ79OFKnmm4Yiumt1oTL6AFSuSAgxFu56Wmg%3D%3D"

def create_sine_variable():
    sine_variables=[]
    for x in range(0, 359):
        weight = math.sin(math.radians(x))*100  # create sine shaped variable in time
        sine_variables.append(weight)
    return sine_variables

def get_cpu_temperature():
    # Return CPU temperature as a character string
    res = os.popen('vcgencmd measure_temp').readline()
    return(float(res.replace("temp=","").replace("'C\n","")))

def get_ip_address():
 ip_address = '';
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address

def fileexists(filename):
        try:
                with open(filename): pass
        except IOError:
                return False 
        return True

def get_temperature(sensor):
        #Routine to read the temperature
        #Read the sensor 10 times checking the CRC until we have a good read 
        for retries in range(0, 10):
                subprocess.call(['modprobe', 'w1-gpio'])
                subprocess.call(['modprobe', 'w1-therm'])

                # Open the file that we viewed earlier so that python can see what is in it. Replace the serial number as bef$
                filename = "/sys/bus/w1/devices/"+sensor+"/w1_slave"
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
    ip_address = get_ip_address()
    while 1:
        try:
            cpu_temp = float("{0:.1f}".format(get_cpu_temperature()))
            sensor1_temp = float("{0:.1f}".format(get_temperature(sensor1_snr)))
            sensor2_temp = float("{0:.1f}".format(get_emperature(sensor2_snr)))
            # ensure that timestamp string is formatted properly
            now = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S%Z")

            # data that we're sending to Power BI REST API
            data = '[{{ "cpu T": {0:0.1f}, "sensor1 T": {1:0.1f}, "sensor2 T": {2:0.1f}, "timestamp": "{3}" }}]'.format(cpu_temp, sensor1_temp, sensor2_temp, now)
#            print(data)
            # make HTTP POST request to Power BI REST API
            req = urllib2.Request(REST_API_URL, data)
            response = urllib2.urlopen(req)
#            print("POST request to Power BI with data:{0}".format(data))
#            print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))

            time.sleep(interval)
        except urllib2.HTTPError as e:
            print("HTTP Error: {0} - {1}".format(e.code, e.reason))
        except urllib2.URLError as e:
            print("URL Error: {0}".format(e.reason))
        except Exception as e:
            print("General Exception: {0}".format(e))


if __name__ == "__main__":
    main()
    sys.exit(0)
