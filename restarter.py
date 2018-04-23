#!/usr/bin/env python3
"""
Check to see if an process is running. If not, restart.
Run this in a cron job
"""
import os

process_name= "toGoogle_rpi2.py" # change this to the name of your process
tmp2 = os.popen("ps -Af").read()

#if process_name not in tmp2:
#    newprocess="sudo nohup python3 /home/jan/toGoogle_rpi2.py"
#    os.system(newprocess)

process_name= "toInitialState.py" # change this to the name of your process
if process_name not in tmp2:
    newprocess="sudo python /home/jan/toInitialState.py"
    os.system(newprocess)

process_name= "toPowerBi.py" # change this to the name of your process
if process_name not in tmp2:
    newprocess="sudo nohup python /home/jan/toPowerBi.py"
    os.system(newprocess)

process_name= "node-red-start" # change this to the name of your process
if process_name not in tmp2:
    newprocess="sudo nohup node-red-start"
    os.system(newprocess)

