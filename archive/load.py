import os
import json
import logging
from datetime import datetime as dt
from dotenv import load_dotenv
import boto3

# setting up files for logging
log_dir = 'logs'
script_name = 'load'
log_timestamp = dt.now().strftime('%Y-%m-%d %H-%M-%S')
os.makedirs(log_dir,exist_ok=True)
os.makedirs(f'{log_dir}/{script_name}',exist_ok=True)
log_filename = f'{log_dir}/{script_name}/{log_timestamp}.log'

# configuration of log file
logging.basicConfig(
    filename = log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # ignore anything below INFO
)

logger = logging.getLogger() 
logger.info('Logger was succesfully initialiser.')

# Connecting to .env to pull through AWS keys
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# # Connecting to .json files (test)
# test_file = 'python-import/test.json'
# test_location = 'unzip_data/100011471/test.json'

# Dynamic file name + connections
data_dir = 'unzip_data/100011471'
file_location = os.listdir(data_dir)

if not file_location:
    print("no .json files to upload to s3. skipping load stage")
    logger.info("no .json files to upload to s3. skipping load stage")
    exit()

# Configuring s3 credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# # Testing whether credentials work
# s3_client.upload_file(
#     test_location, AWS_BUCKET_NAME, test_file
# )

# For each file in data_dir ...
for file in file_location:
    upload_location = f'{data_dir}/{file}'
    upload_name = f'python-import/{file}'
    
    try:
        s3_client.upload_file(
            upload_location
            , AWS_BUCKET_NAME
            , upload_name)
        os.remove(upload_location)
        print(f'File {file} successfully uploaded!')
        logger.info(f'File {file} successfully uploaded!')
    except Exception as e:
        print(f'Something went wrong... Error: {e}')
        logger.error(f'Something went wrong... Error: {e}')

