#!/usr/bin/env python3

'''
sending temperature sensor data from myraspi to InitialState.com account jan.kempeneers2@gmail.com
'''

import os
import sys
import math
import time
import subprocess
import socket
from ISStreamer.Streamer import Streamer

streamer = Streamer(bucket_name="myHome", bucket_key="8DAJL478FHKN", access_key="nWHNn1mOEia5I98FopFAiArcE0ZHMcKW")

sensor1_snr = "28-0416939b61ff" # unique sensor id nr
sensor2_snr = "28-051692afcaff" # unique sensor id nr
interval = 5*60 # sending interval time in seconds
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
        # Routine to read the temperature
        # Read the sensor 10 times checking the CRC until we have a good read 
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
        # If after 10 tries we were unable to get a good read return 0
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
    streamer.log("My Messages", "IP address = {}".format(ip_address))
    while 1:
        cpu_temp = float("{0:.1f}".format(get_cpu_temperature()))
        sensor1_temp = float("{0:.1f}".format(get_temperature(sensor1_snr)))
        sensor2_temp = float("{0:.1f}".format(get_temperature(sensor2_snr)))
#        print("cpu temp = {0:.1f};   sensor1_temp = {1:.1f};   sensor2_temp = {2:.1f}".format(cpu_temp, sensor1_temp, sensor2_temp))
        streamer.log("cpu temp", cpu_temp)
        streamer.log("sensor1 T", sensor1_temp)
        streamer.log("sensor2 T", sensor2_temp)
        streamer.flush
        time.sleep(interval)
streamer.close

if __name__ == "__main__":
    main()
    sys.exit(0)
