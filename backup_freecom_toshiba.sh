#!/bin/bash


rsync -avs --delete -i --exclude 'Hydromation' --exclude 'nds games' "/media/freecom/jakem data" "/media/toshiba"
echo $(date) | tee -a /home/jan/backup_freecom_toshiba.log

