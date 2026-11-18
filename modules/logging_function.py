import os
import logging

logger = logging.getLogger(__name__)

def logging_config(log_dir: str, log_timestamp: str):
    """Function to configure logging

    Args:
        log__dir (str): where logs are saved
        log_timestamp (str): timestamp used for naming log file (usually time of running)
    """
    os.makedirs(log_dir,exist_ok=True)
    log_filename = f'{log_dir}/{log_timestamp}.log'

    # configuration of log file
    logging.basicConfig(
        filename = log_filename,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO # ignore anything below INFO
    )