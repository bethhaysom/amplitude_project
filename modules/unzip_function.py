import os
import logging
import gzip
import zipfile
import shutil
import tempfile

logger = logging.getLogger(__name__)

def zip_to_json(data_dir: str, unzip_dir: str):
    """Function to unzip .zip file, then un-gzip, saving inner .json files to destination. Returns false if no files to unzip.

    Args:
        data_dir (str): filepath to existing .zip files
        unzip_dir (str): filepath to save output .json files to
    """
    
    # locating the .zip file we need
    data_dir = os.path.abspath(f'c:{data_dir}')

    # Find all .zip archives in data_dir (automatically ignores the Archive folder)
    zip_files = [
        f for f in os.listdir(data_dir) if f.endswith('.zip')
        ]

    if not zip_files:
        logger.info(".zip files are all unzipped already. Skipping unzip stage.")
        return False
    
    else:
        # Create a temporary directory for extraction
        temp_dir = tempfile.mkdtemp()

        # Create local output directory
        os.makedirs(unzip_dir, exist_ok=True)

        # for each .zip in /data, want to .extractall
        for zip_name in zip_files:
            file_zip = os.path.join(data_dir, zip_name) #single string path for each zip file
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
                                logger.info(f'{json_path} extracted - yay!')

        shutil.move(file_zip, os.path.join(temp_dir, os.path.basename(file_zip)))
        shutil.rmtree(temp_dir)
        logger.info(f'Removed {file_zip} and saved all .json files to {unzip_dir}')
        return True