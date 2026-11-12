import os
import time
import logging
from datetime import datetime as dt, timedelta
import requests 
from dotenv import load_dotenv

yesterday = dt.now() + timedelta(days=-1)
timestamp = yesterday.strftime('%Y-%m-%d %H-%M-%S')
start_date = yesterday.strftime('%Y%m%dT00')
end_date = yesterday.strftime('%Y%m%dT23')


# setting up files for logging
log_dir = 'logs'
os.makedirs(log_dir,exist_ok=True)
log_filename = f'{log_dir}/{timestamp}.log'

# configuration of log file
logging.basicConfig(
    filename = log_filename,
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO # ignore anything below INFO
)

logger = logging.getLogger() 
logger.info('Logger was succesfully initialiser.')


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
            logger.error
        attempt += 1
        time.sleep(30)