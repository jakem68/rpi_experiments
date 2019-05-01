#!/usr/bin/env python3
"""
Check to see if a process is running. If not, restart.
Run this in a cron job
"""
import os

tmp2 = os.popen("ps -Af").read()

#process_name= "sensor_temp_toGoogle_rpi.py" # change this to the name of your process
#if process_name not in tmp2:
#    newprocess="sudo nohup python /home/jan/sensor_temp_toGoogle_rpi.py"
#    os.system(newprocess)

process_name= "rrd_toGoogle_rpi.py" # change this to the name of your process
if process_name not in tmp2:
    newprocess="sudo nohup python /home/pi/programs/rrd_toGoogle_rpi.py"
    os.system(newprocess)

process_name= "temperature_to_dweet.py" # change this to the name of your process
if process_name not in tmp2:
    newprocess="sudo nohup python /home/pi/programs/temperature_to_dweet.py"
    os.system(newprocess)
