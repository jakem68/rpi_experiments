#!/usr/bin/env python

import time
import grovepi

from grovepi import *
from grove_rgb_lcd import *
from time import sleep
from math import isnan

# set green as backlight color
# we need to do it just once
# setting the backlight color once reduces the amount of data transfer over the I2C line
setRGB(0,255,0)


# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0

# my_string can be any text that will be shown on the display one line at a time
#my_text = "Hello Victoria, \n first of all  best wishes for your birthday \n but this Raspberry Pi is meant to be more \n than just a wishing card :-)"
with open('wishes.txt', 'r') as myfile:
    my_text=myfile.read()

# Connect the LED to digital port D5
# SIG,NC,VCC,GND
led = 5

grovepi.pinMode(potentiometer,"INPUT")
grovepi.pinMode(led,"OUTPUT")
time.sleep(1)

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

# Full value of the rotary angle is 300 degrees, as per it's specs (0 to 300)
full_angle = 300

def calculate_degrees_potentiometer():
    # Read sensor value from potentiometer
    sensor_value = grovepi.analogRead(potentiometer)

    # Calculate voltage
    voltage = round((float)(sensor_value) * adc_ref / 1023, 2)

    # Calculate rotation in degrees (0 to 300)
    degrees = round((voltage * full_angle) / grove_vcc, 2)
    
    return degrees

def calculate_line_to_show():
    current_degree = calculate_degrees_potentiometer()
    # construction to always round up: first always round down than add boolean result 0 or 1 based on evaluation of remainder
    line_to_show = int(current_degree/degrees_per_line) + (current_degree % degrees_per_line > 0)
    if line_to_show >= len(splitted_text):
        line_to_show = len(splitted_text)-1
    return line_to_show

def calcBG(degrees):
    "This calculates the color value for the background"
    variance = full_angle - degrees - 150;   # Calculate the variance
#    adj = calcColorAdj(variance);   # Scale it to 8 bit int
    adj = int(degrees/300*255)
    bgList = [0,0,0]               # initialize the color array
    if(variance < 0):
        bgR = 0;                    # too cold, no red
        bgB = adj;                  # green and blue slide equally with adj
        bgG = 255 - adj;
        
    elif(variance == 0):             # perfect, all on green
        bgR = 0;
        bgB = 0;
        bgG = 255;
        
    elif(variance > 0):             #too hot - no blue
        bgB = 0;
        bgR = adj;                  # Red and Green slide equally with Adj
        bgG = 255 - adj;
        
    bgList = [bgR,bgG,bgB]          #build list of color values to return
    return bgList;


splitted_text = my_text.splitlines()
print (splitted_text)
number_of_lines = len(splitted_text)
degrees_per_line = int(full_angle/number_of_lines)

while True:
    try:
        line_to_show = calculate_line_to_show()
        print (splitted_text[line_to_show])

        degrees = calculate_degrees_potentiometer()

        # Calculate LED brightess (0 to 255) from degrees (0 to 300)
        brightness = int(degrees / full_angle * 255)

        # Give PWM output to LED
        grovepi.analogWrite(led,brightness)

        # calculate and set background colour
        bgList = calcBG(degrees)           # Calculate background colors
        setRGB(bgList[0],bgList[1],bgList[2])   # parse our list into the color settings

        setText_norefresh(splitted_text[line_to_show])

#        print("sensor_value = %d voltage = %.2f degrees = %.1f brightness = %d" %(sensor_value, voltage, degrees, brightness))
    except KeyboardInterrupt:
        grovepi.analogWrite(led,0)
        break
    except IOError:
        print ("Error")

