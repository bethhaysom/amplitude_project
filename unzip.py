import os
import gzip
import json
import zipfile
import shutil
import tempfile
from datetime import datetime as dt, timedelta
import requests 
from dotenv import load_dotenv

yesterday = dt.now() + timedelta(days=-1)
timestamp = yesterday.strftime('%Y-%m-%d') # will want a loop that cycles through data folder and gives list of zips in there

# locating the .zip file we need
data_dir = os.path.abspath('c:data')
file_zip = f'{data_dir}/{timestamp}.zip'

# Create a temporary directory for extraction
temp_dir = tempfile.mkdtemp()

# Create local output directory
unzip_dir = "unzip_data"
os.makedirs(unzip_dir, exist_ok=True)

# for each .zip in /data, want to .extractall
with zipfile.ZipFile(file_zip, 'r') as zip_ref:
    zip_ref.extractall(temp_dir) # extracts .zip to temp_dir
    data_zip = zip_ref.namelist()    # returns name of all .gz files in .zip

    # within the .zip, for each .gz file, get path name
    # open each .gz and decompress
    # save final as .json
    for filename in data_zip: # will do through each file in .zip
        if filename.endswith('.gz'):
            gz_path = os.path.join(temp_dir, filename) # full path to extracted .gz

            # checking is file ends with .json and removing the .gz at end of file name
            if filename.endswith('.json.gz'):
                json_filename = filename[:-3]
            else:
                json_filename = os.path.splitext(filename)[0] + '.json'

            json_path = os.path.join(unzip_dir, json_filename)
            
            # Ensure any subfolders inside the zip also exist in unzip_dir
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            
            # opening the .gz file and writing the decompressed data to the .json file
            with gzip.open(gz_path, 'rb') as f_in: # opens .gz to read
                with open(json_path, 'wb') as f_out: # opens .json to write
                    shutil.copyfileobj(f_in, f_out) # moves bytes from .gz to .json
                    print(f'{json_path} extracted - yay!')

shutil.rmtree(temp_dir)
