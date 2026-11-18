import os
import time
import logging
import re
from modules.logging_function import logging_config
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