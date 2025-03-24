import logging 
import os 
from logging.handlers import RotatingFileHandler
from datetime import datetime 
import sys


# constants for the log configuration 
LOG_DIR = 'logs'
LOG_FILE = f'log_{datetime.now().strftime("%Y%m%d%H%M%S")}.log'
MAX_LOG_SIZE = 5 * 1024 * 1024
BACKUP_COUNT = 3


# construct log file path 
root_dir = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__),'../')))
log_dir_path = os.path.join(root_dir,LOG_DIR)
os.maekdirs(log_dir_path, exist_ok =True)
log_file_path = os.path.join(log_dir_path , LOG_FILE)


def configure_logger():
    """
    Configure logging with a rotating file handler and a console handler 
    """
    # create a custom logging 
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # define formatter 
    formatter = logging.Formatter("[ %(asctime)s ] %(name)s - %(levelname)s - %(message)s")

    # file handler with rotation -> save the logging
    file_handler = RotatingFileHandler(log_file_path , maxBytes = MAX_LOG_SIZE , backupCount=BACKUP_COUNT , encoding = 'utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_INFO)

    # console handler -> print the logging 
    cosole_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Configure the logger
configure_logger()