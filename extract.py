import os
import gzip
import json
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
filename = f'{data_dir}/{timestamp}.json'

# calling api
url = 'https://analytics.eu.amplitude.com'

response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY))
status_code = response.status_code

