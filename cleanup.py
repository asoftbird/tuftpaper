import os
import shutil
import json
import logging
from datetime import date

with open("config.json") as cfgfile:
    CFG = json.load(cfgfile)

LOGFILE=CFG["log-file-cleanup"]
OUTPUT_DIR=CFG["output-dir"]
ARCHIVE_DIR=CFG["archive-dir"]

logging.basicConfig(filename=LOGFILE, 
    encoding='utf-8', 
    level=logging.INFO, 
    format='%(asctime)s %(message)s',
    datefmt='[%a %d-%m-%y %H:%M:%S]'
    )

current_date = date.today()
day = str(current_date.day).zfill(2)
month = str(current_date.strftime("%b")).zfill(2)
date_today = day + "-" + month
date_yesterday = str(int(day)-1) + "-" + month

# check if there's enough pictures for today. if not: leave yesterday's images in place
files_today = 0
for filename in os.listdir(OUTPUT_DIR):
    if filename.startswith(date_today):
        files_today += 1

counter = 0
for filename in os.listdir(OUTPUT_DIR): 
    if files_today <= 8: 
        if not filename.startswith(date_today) and not filename.startswith(date_yesterday):
            counter += 1
            shutil.move(os.path.join(OUTPUT_DIR, filename), os.path.join(ARCHIVE_DIR, filename))
            #logging.info(f"Moved {filename} to archive.")
    else:
        if not filename.startswith(date_today):
            counter += 1
            shutil.move(os.path.join(OUTPUT_DIR, filename), os.path.join(ARCHIVE_DIR, filename))
            #logging.info(f"Moved {filename} to archive.")
    
logging.info(f"Moved {counter} files to archive.")