import logging
import os
from datetime import datetime

# The file name which will be created in the folder
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# The folder which will be created
log_path = os.path.join(os.getcwd(), 'logs')

# Make the folder
os.makedirs(log_path, exist_ok=True)

# Connect the folder path with the file name to have a complete path
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Format: contains what will be returned
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE_PATH,
    format='[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s'
)
                    