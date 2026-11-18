import logging
import re
from datetime import datetime as dt, timedelta
import boto3

logger = logging.getLogger(__name__)


def checking_s3_files(AWS_ACCESS_KEY: str, AWS_SECRET_ACCESS_KEY: str, AWS_BUCKET_NAME: str, prefix: str, default_date: dt, yesterday: dt):
    """Function for checking existing files in s3 to establish missing dates. returns start date if exists (or none if not)

    Args:
        AWS_ACCESS_KEY (str): key value (get value from .env)
        AWS_SECRET_ACCESS_KEY (str): secret key value (get value from .env)
        AWS_BUCKET_NAME (str): S3 bucket name (get value from .env)
        prefix (str): folder name in bucket (needs to be in format '<foldername>/')
        default_date (dt): earliest date wanted for data stored in s3
        yesterday (ds): most recent date wanted for files in s3
    """
    # Configuring s3 credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )

    response = s3_client.list_objects_v2(Bucket=AWS_BUCKET_NAME, Prefix=prefix)

    # Filter for .json files in Python (S3 doesn't filter by suffix natively)
    json_files = [
        obj["Key"]
        for obj in response.get("Contents", [])
        if obj["Key"].endswith(".json")
    ]
    logger.info(json_files)

    # Find max date in filenames
    max_date = max(
        (
            dt.strptime(match.group(1), "%Y-%m-%d").date()
            for key in json_files
            if (match := re.search(r"(\d{4}-\d{2}-\d{2})", key))
        ),
        default=None
    )
    logger.info(f'Max date in s3 = {max_date}')
   
    # start date function: if x < yesterday then x+1 else yesterday
    default_start = default_date

    if max_date is None:
        start = default_start
        return start
    elif max_date < yesterday:
        start = max_date + timedelta(days=1)
        return start
    else:
        logger.warning("S3 is already up to date through yesterday. Skipping API call.")
        return None
