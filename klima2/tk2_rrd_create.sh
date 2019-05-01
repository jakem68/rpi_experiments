#!/bin/bash

rrdtool create '/home/pi/programs/temp_klima2.rrd' \
    --step 60 \
    DS:temp_klima2:GAUGE:120:U:U \
    RRA:LAST:0.5:1:525600 \
    RRA:AVERAGE:0.5:1440:1825
