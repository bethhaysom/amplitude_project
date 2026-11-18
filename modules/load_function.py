import os
import logging
import boto3

logger = logging.getLogger(__name__)

def load_to_s3(data_dir: str, prefix: str, AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str):
    """Function to upload files to S3

    Args:
        data_dir (str): filepath to find saved data
        prefix (str): folder name in bucket (needs to be in format '<foldername>/')
        AWS_ACCESS_KEY (str): key value (get value from .env)
        AWS_SECRET_ACCESS_KEY (str): secret key value (get value from .env)
        AWS_BUCKET_NAME (str): S3 bucket name (get value from .env)
    """

    file_location = os.listdir(data_dir)

    # Configuring s3 credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    # For each file in data_dir ...
    for file in file_location:
        upload_location = f'{data_dir}/{file}'
        upload_name = f'{prefix}{file}'
        
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

