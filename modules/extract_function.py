import os
import time
import logging
import requests 

logger = logging.getLogger(__name__)

def extract_to_zip(AMP_API_KEY: str, AMP_SECRET_KEY: str, params: dict, url: str, data_dir: str, timestamp: str, max_attempts: int, delay: int):
    """Function to extract .zip files from a URL using an API that requires keys and parameters, and saving to a destination 

    Args:
        AMP_API_KEY (str): API key value (get value from .env)
        AMP_SECRET_KEY (str): API secret key value (get value from .env)
        params (dict): required parameters for API call (check api documentation)
        url (str): URL to pull data from API
        data_dir (str): filepath to save data to
        timestamp (str): timestamp to append to filename
        max_attempts (int): number of times to retry API call
        delay (int): how long to wait between call attempts
    """

    # File configuration
    os.makedirs(data_dir,exist_ok=True)
    filename = f'{data_dir}/{timestamp}.zip'

    attempt = 1

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

                # flag that data was saved successfully
                return True
            
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

    # return statement if unsuccessful
    return False