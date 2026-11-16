import os
import json
import logging
from dotenv import load_dotenv
import boto3

# Connecting to .env to pull through AWS keys
load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

# Connecting to .json files (test)
test_file = 'python-import/test.json'
test_location = 'unzip_data/100011471/test.json'

# Configuring s3 credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# Testing whether credentials work
s3_client.upload_file(
    test_location, AWS_BUCKET_NAME, test_file
)
