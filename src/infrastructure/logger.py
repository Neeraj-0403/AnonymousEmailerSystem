# infrastructure/logger.py

import logging
import os
from datetime import datetime

# Define a log file path.
LOG_FILE = "logs/system_log.log"

# Set up the logger.
def setup_logger():
    """Configures the application-wide logger."""
    try:
        # if os.path.exists(LOG_FILE):
        #     os.rename(LOG_FILE, f"system_log_old_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

        # Create the logger
        logger = logging.getLogger('anonymous_email_sender')
        logger.setLevel(logging.DEBUG)

        # Create file handler
        fh = logging.FileHandler(LOG_FILE)
        fh.setLevel(logging.DEBUG)

        # Create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

        return logger

    except Exception as e:
        # Fallback to a basic logger setup
        print(f"Error setting up logger: {e}")
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger('fallback_logger')

# Global logger instance
logger = setup_logger()
