import time
import RPi.GPIO as GPIO
import subprocess
import dweepy
import socket

sensor_snr = "28-051692d95eff"
interval = 10

def fileexists(filename):
        try:
                with open(filename): pass
        except IOError:
                return False
        return True

def GetTemperature():
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

def get_ip():
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ip = s.getsockname()[0]
	s.close()
	return(ip)


while 1:
    reading = GetTemperature()
    ip = get_ip()
#    values = (time.strftime('%d/%m/%Y %H:%M:%S'), reading)
    values = {"timestamp":time.time(), "temp":reading, "IP address":ip}
    dweepy.dweet_for("rpi_klima2", values)
    print values
    time.sleep(interval)
