import os
import gzip
import json
import zipfile
from datetime import datetime as dt, timedelta
import requests 
from dotenv import load_dotenv

yesterday = dt.now() + timedelta(days=-2)
timestamp = f'2026-11-11 17-30-47' # will want a loop that cycles through data folder and gives list of zips in there

data_dir = os.path.abspath('c:data')
file_zip = f'{data_dir}/{timestamp}.zip'

# for each .zip in /data, want to .extractall
with zipfile.ZipFile(file_zip, 'r') as zip_ref:
    # zip_ref.extractall(data_dir) # extracts .zip
    data_zip = zip_ref.namelist()    # returns name of all .gz files in .zip

    # within the .zip, for each .gz file, get path name
    # open each .gz and decompress
    # save final as .json
    for n in range(0,23): # will do through each hourly file in .zip
        data_nzip = data_zip[n]
        print(data_nzip)
        # hourly = f'{file_zip}/{data_nzip}' # file path for .gz files
        # with gzip.open(hourly[n], 'wb') as file: # opening .gz
        #     file.write(data_nzip) # writing file

