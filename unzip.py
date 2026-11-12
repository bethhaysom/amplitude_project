import os
import gzip
import json
import zipfile
from datetime import datetime as dt, timedelta
import requests 
from dotenv import load_dotenv

data_dir = os.path.abspath('c:data')
file_zip = f'{data_dir}/2026-11-11 17-30-47.zip'

with zipfile.ZipFile(file_zip, 'r') as zip_ref:
    # zip_ref.extractall(data_dir)
    print(zip_ref.namelist())        
    # unzip outer file