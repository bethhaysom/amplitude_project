import os
import time
import logging
import re
from datetime import datetime as dt, timedelta
import requests 
from dotenv import load_dotenv
import boto3

# date configuration:
yesterday = dt.now().date() + timedelta(days=-1)
timestamp = yesterday.strftime('%Y-%m-%d')

#-----------------------------------------------------------------------------
# setting up files for logging
log_dir = 'logs'
log_timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{log_timestamp}.log'

# configuration of log file
logging.basicConfig(
    filename = log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # ignore anything below INFO
)

logger = logging.getLogger() 
logger.info('Logger was succesfully initialiser.')

#-----------------------------------------------------------------------------
# Checking existing s3 files:
# Connect to s3 bucket
# Connecting to .env to pull through AWS keys
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Configuring s3 credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
bucket_name = AWS_BUCKET_NAME
prefix = 'python-import/'


# list file names 
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
# Filter for .json files in Python (S3 doesn't filter by suffix natively)
json_files = [
    obj["Key"]
    for obj in response.get("Contents", [])
    if obj["Key"].endswith(".json")
]
#print(json_files)

# remove letters at start of file name
# isolate date and change into date format / matching start/end format
# select max date as x
max_date = max(
    (
        dt.strptime(match.group(1), "%Y-%m-%d").date()
        for key in json_files
        if (match := re.search(r"(\d{4}-\d{2}-\d{2})", key))
    ),
    default=None
)

# start date function: if x < yesterday then x+1 else yesterday
default_start = dt(2026, 11, 15).date() # added in case there is nothing in the s3 bucket currently

if max_date is None:
    start = default_start
elif max_date < yesterday:
    start = max_date + timedelta(days=1)
else:
    print("S3 is already up to date through yesterday. Skipping API call.")
    exit()


start_date = start.strftime('%Y%m%dT00')
end_date = yesterday.strftime('%Y%m%dT23')
print(start_date)
print(end_date)

#-----------------------------------------------------------------------------
# api configuration
load_dotenv()

AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

params = {
    'start': f'{start_date}',
    'end': f'{end_date}'
}

# configure output file
data_dir = 'data'
os.makedirs(data_dir,exist_ok=True)
filename = f'{data_dir}/{timestamp}.zip'

# calling api
url = 'https://analytics.eu.amplitude.com/api/2/export'

#-----------------------------------------------------------------------------
# checking attempt numbers
attempt = 1
max_attempts = 3

while attempt <= max_attempts:
    # calling API
    response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY))
    status_code = response.status_code

    # handling status codes
    if 200 <= status_code < 300: # request recieved successfully
        try:
            data_z = response.content # getting zipped file from api

            # saving zipped file
            with open(filename, 'wb') as file:
                file.write(data_z)
                
            print(f'file {filename} saved successfully')
            logger.info(f'file {filename} saved successfully - yay!')

        except Exception as e:
            print(f'An error occurred when saving the .zip: {e}')
            logger.error(f'An error occurred when saving the .zip: {e}')
        break

    elif 300 <= status_code < 500: # issue that means the api can't be run
        print(f'API call failed, status code {status_code}')
        logger.error(f'API call failed, status code {status_code}')
        break

    else:
        if attempt == max_attempts:
            print(f'Max number of attempts reached. Status code {status_code}. Investigate further pls.')
            logging.warning(f'Max number of attempts reached. Status code {status_code}. Investigate further pls.')
        else: 
            print(f'Attempt {attempt} failed, status code {status_code}. Trying again...')
            logger.error(f'Attempt {attempt} failed, status code {status_code}. Trying again...')
        attempt += 1
        time.sleep(delay)

