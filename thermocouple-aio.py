#!/usr/bin/python3
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client('jankempeneers', '0642323bbbf34022955dd1f38024dfce')
oven_temperature = aio.feeds('sirris10-amifv2.sirris10-amifv2-oven-temperature')
# interval at which data will be sent to Adafruit in seconds
interval = 60


# Define a function to convert celsius to fahrenheit.
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

# A function to check for NaN
def isNaN(num):
    return num != num


# Uncomment one of the blocks of code below to configure your Pi or BBB to use
# software or hardware SPI.

# Raspberry Pi software SPI configuration.
CLK = 25
CS  = 24
DO  = 18
sensor = MAX31855.MAX31855(CLK, CS, DO)

# Loop printing measurements every second.
print('Press Ctrl-C to quit.')
while True:
    temp = sensor.readTempC()
    internal = sensor.readInternalC()
#    print('Thermocouple Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(temp, c_to_f(temp)))
#    print('    Internal Temperature: {0:0.3F}*C / {1:0.3F}*F'.format(internal, c_to_f(internal)))
    print('Thermocouple Temperature: {0:0.3F}*C'.format(temp))
    # Add the value 98.6 to the feed 'Temperature'.
    if not isNaN(temp):
        try:
            aio.send_data(oven_temperature.key, temp)
            errorcount = 0
        except:
            print("Some error, let's wait a little longer")
            errorcount += 1
            time.sleep(10.0)
            if errorcount > 10:
                print("error has occured more than 10 times, I am quitting")
                break
            pass

    time.sleep(interval)
