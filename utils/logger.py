import logging
import os
from datetime import datetime

def setup_logger(log_dir="logs", level=logging.INFO):
    """Set up application logging with file and console handlers."""
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create a unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"qa_agent_{timestamp}.log")
    
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.WARNING)  # Only warnings and above to console
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logging.info(f"Logging configured. Log file: {log_file}")
    return logger 