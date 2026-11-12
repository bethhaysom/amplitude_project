import os
import gzip
import json
import zipfile
from datetime import datetime as dt
import requests 
from dotenv import load_dotenv

timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')

load_dotenv()

AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

params = {
    'start': '20261110T00',
    'end': '20261110T23'
}

# configure output file
data_dir = 'data'
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.zip'

# calling api
url = 'https://analytics.eu.amplitude.com/api/2/export'


# checking attempt numbers
attempt = 1
max_attempts = 3

while attempt <= max_attempts:
    # calling API
    response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY))
    status_code = response.status_code

    # handling status codes
    if 200 <= status_code < 300: # request recieved successfully
        
        data_z = response.content # getting zipped file from api

        # saving zipped file
        with open(filename, 'wb') as file:
            file.write(data_z)
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                # zip_ref.extractall(data_dir)
                print(zip_ref.namelist())        
            # unzip outer file
        print(f'file {filename} saved successfully')

    elif 300 <= status_code < 500: # issue that means the api can't be run
        print(f'API call failed, status code {status_code}')

    else:
        print(f'API failed, status code {status_code}')

