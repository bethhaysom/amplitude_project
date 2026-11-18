import os
import time
import logging
import re
from modules.logging_function import logging_config
from modules.s3_filecheck_function import checking_s3_files
from modules.extract_function import extract_to_zip
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

logging_config(log_dir, log_timestamp)

logger = logging.getLogger() 
logger.info('Logger was succesfully initialiser.')

#-----------------------------------------------------------------------------
# Variable configuration:

# collecting secrets
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

# for s3 check
prefix = 'python-import/'
default_date = dt(2026, 11, 15).date()

# for extraction
data_dir = 'data'

url = 'https://analytics.eu.amplitude.com/api/2/export'

max_attempts = 3
delay = 30


#-----------------------------------------------------------------------------
# Checking existing s3 files:

s3_check = checking_s3_files(
    AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_BUCKET_NAME, prefix, default_date, yesterday
    )

if s3_check is None: 
    exit() # means S3 is already up to date through yesterday. Skipping API call.
else:
    start = s3_check

start_date = start.strftime('%Y%m%dT00')
end_date = yesterday.strftime('%Y%m%dT23')
logging.info(f'start date defined as {start_date}, end date defined as {end_date}')

# set params for api call
params = {
    'start': f'{start_date}',
    'end': f'{end_date}'
}

#-----------------------------------------------------------------------------
# Calling API
extract_result = extract_to_zip(
    AMP_API_KEY, AMP_SECRET_KEY, params, url, data_dir, timestamp, max_attempts, delay
    )

print(extract_result)