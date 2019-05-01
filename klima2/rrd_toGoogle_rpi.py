#!/usr/bin/env python

'''
adds a value to rrd file and creates a new graph picture
and updates picture in rpi google account
'''
import os
import sys
import time
import rrdtool
import subprocess
from serv_acc_update_file import update_google_graph

# result = rrdtool.fetch('/home/jan/klima1_temperatuur.rrd', 'AVERAGE')
# print(result)
rrd_file = '/home/pi/programs/temp_klima2.rrd' #file previously created from CLI, 1yr of measurements per min, 5yr of average per day
sensor_snr = '28-051692d95eff'

def rrd_update(rrd_file, value):
    ret = rrdtool.update(rrd_file, 'N:' + str(value))
#    if ret:
#        print("rrdtool error")

def rrd_graph_update_1d(rrd_file):
     subprocess.check_call(['/home/pi/programs/tk2_graph_1d.sh', rrd_file])

def rrd_graph_update_1w(rrd_file):
     subprocess.check_call(['/home/pi/programs/tk2_graph_1w.sh', rrd_file])

def rrd_graph_update_1m(rrd_file):
     subprocess.check_call(['/home/pi/programs/tk2_graph_1m.sh', rrd_file])

def rrd_graph_update_1m_average(rrd_file):
     subprocess.check_call(['/home/pi/programs/tk2_graph_1m_average.sh', rrd_file])

def rrd_graph_update_1y_average(rrd_file):
     subprocess.check_call(['/home/pi/programs/tk2_graph_1y_average.sh', rrd_file])

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

def update_all():
    #Google files
    file_IDs = ['0B2QAUBy5MV9rUFJQbVdaUXBTMVk',
                '0B2QAUBy5MV9rNVdQb2NrZC00Rm8',
                '0B2QAUBy5MV9rT0UtS2tiUHFDTTA',
                '0B2QAUBy5MV9rTjB4aXB4MEFtOHM',
                '0B2QAUBy5MV9rV0dGY1ZCeDItMk0']
    #local files
    filesources = ['/home/pi/programs/tk2_graph_1d.png',
                   '/home/pi/programs/tk2_graph_1w.png',
                   '/home/pi/programs/tk2_graph_1m.png',
                   '/home/pi/programs/tk2_graph_1m_average.png',
                   '/home/pi/programs/tk2_graph_1y_average.png',]
    while True:
        my_temp = get_sensor_temperature()
        rrd_update(rrd_file, my_temp)
	rrd_graph_update_1d(rrd_file)
	time.sleep(5)
        rrd_graph_update_1w(rrd_file)
	time.sleep(5)
        rrd_graph_update_1m(rrd_file)
	time.sleep(5)
        rrd_graph_update_1m_average(rrd_file)
	time.sleep(5)
        rrd_graph_update_1y_average(rrd_file)
	time.sleep(5)
        for i in range(0, len(file_IDs)):
            update_google_graph(file_IDs[i], filesources[i])
	    time.sleep(35/len(file_IDs))

def main():
    update_all()
    sys.exit(0)


if __name__ == "__main__":
    main()
