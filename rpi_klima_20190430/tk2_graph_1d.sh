#!/bin/bash

rrd_file=$1
#echo $rrd_file
rrdtool graph '/home/pi/programs/tk2_graph_1d.png' \
  --title "Last day" \
  --slope-mode \
  --start -1d \
  --end now \
  --alt-autoscale \
  --vertical-label "Temperature" \
  --right-axis 1:0 \
  --right-axis-format "%2.0lf" \
  --right-axis-label "Temperature" \
  -w 800 -h 300 \
  DEF:tk2=$rrd_file:temp_klima2:LAST \
  VDEF:tk2_last=tk2,LAST \
  VDEF:tk2_max=tk2,MAXIMUM \
  VDEF:tk2_min=tk2,MINIMUM \
  VDEF:tk2_avg=tk2,AVERAGE \
  LINE:tk2_avg \
  AREA:tk2#dbe5ff:"" \
  LINE:tk2#4286f4:"T klima 2" \
  GPRINT:tk2_last:"Last measurement %d/%m/%y %H\:%M\:%S:strftime" \
  GPRINT:tk2_last:"Current T = %2.1lf C" \
  GPRINT:tk2_max:"Max T = %2.1lf C" \
  GPRINT:tk2_min:"Min T = %2.1lf C" \
  GPRINT:tk2_avg:"Avg T = %2.1lf C" \
  HRULE:tk2_avg#cccccc:"average":dashes=5
