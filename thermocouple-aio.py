#!/usr/bin/python3
# Copyright (c) 2014 Adafruit Industries - Author: Tony DiCola


import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855
from Adafruit_IO import Client
import sys
sys.path.insert(0, "..")
from opcua import ua, Server

# Configuration of Adafruit-IO Client and feed.
aio = Client('jankempeneers', '0642323bbbf34022955dd1f38024dfce')
oven_temperature = aio.feeds('sirris10-amifv2.sirris10-amifv2-oven-temperature')

# Configuration of Raspberry Pi software SPI.
CLK = 25
CS  = 24
DO  = 18
sensor = MAX31855.MAX31855(CLK, CS, DO)

# Interval at which data will be sent to Adafruit and opcua-server in seconds.
interval_adafruit = 300
interval_opcua = 1
interval_errorwait = 10
interval_programloop = 0.1
adafruit_send_retries = 10

programloops_per_adafruit = interval_adafruit/interval_programloop
programloops_per_opcua = interval_opcua/interval_programloop
counter_programloops_adafruit = 0
counter_programloops_opcua = 0

# A function to convert celsius to fahrenheit.
def c_to_f(c):
    return c * 9.0 / 5.0 + 32.0

# A function to check for NaN
def isNaN(num):
    return num != num


# A function to start opcua server (is blocking must be run in separate thread).
def start_opcua_server():
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/sirris/server/")

    # setup our own namespace, not really necessary but should as spec
    uri = "http://examples.sirris.github.io"
    idx = server.register_namespace(uri)

    # get Objects node, this is where we should put our nodes
    objects = server.get_objects_node()

    # populating our address space
    myobj = objects.add_object(idx, "AMIF_oven")
    myvar = myobj.add_variable(idx, "oven_temperature", 6.7)
    myvar.set_writable()    # Set MyVariable to be writable by clients
    # q.put(myvar)

    # starting!
    server.start()

    return myvar

def time_to_inform_opcua():
    global counter_programloops_opcua
    global programloops_per_opcua
    if counter_programloops_opcua > programloops_per_opcua:
        counter_programloops_opcua = 0
        return True
    else:
        print('counter programloops opcua is {}'.format(counter_programloops_opcua))
        counter_programloops_opcua += 1
        return False

def time_to_inform_adafruit():
    global counter_programloops_adafruit
    global programloops_per_adafruit
    if counter_programloops_adafruit > programloops_per_adafruit:
        counter_programloops_adafruit = 0
        return True
    else:
        print('counter programloop adafruit is {}'.format(counter_programloops_adafruit))
        counter_programloops_adafruit += 1
        return False

def inform_adafruit(temp):
    if not isNaN(temp):
        try:
            aio.send_data(oven_temperature.key, temp)
            errorcount = 0
        except:
            print("Some error, let's wait a little longer")
            errorcount += 1
            time.sleep(interval_errorwait)
            if errorcount > adafruit_send_retries:
                print("error has occured more than 10 times, I am quitting")
            pass

def inform_opcua(myvar, temp):
    myvar.set_value(temp)


def main():
    # q = Queue.Queue()
    # thread1 = threading.Thread(target=start_opcua_server, args=(q))
    # thread1.start()
    # time.sleep(0.1)
    # myvar = q.get()
    myvar = start_opcua_server()
    while True:
        temp = sensor.readTempC()
        internal = sensor.readInternalC()
        print('Thermocouple Temperature: {0:0.3F}*C'.format(temp))
        if time_to_inform_adafruit():
            inform_adafruit(temp)
        
        if time_to_inform_opcua():
            inform_opcua(myvar, temp)

        time.sleep(interval_programloop)

if __name__ == "__main__":
    main()
