# src/detection/utils.py

import os
import logging
from .config import LOG_DIR, DETECTION_LOG_FILE, LOGGING_LEVEL, LOGGING_FORMAT
from .exceptions import UnsupportedFileFormatError

def setup_logging():
    """
    Sets up logging with both file and console handlers.
    Ensures that the log directory exists.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DETECTION_LOG_FILE), exist_ok=True)
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOGGING_LEVEL.upper(), logging.INFO))
    
    # File Handler
    file_handler = logging.FileHandler(DETECTION_LOG_FILE)
    file_formatter = logging.Formatter(LOGGING_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(LOGGING_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def validate_file_path(file_path, supported_formats):
    """
    Validates if the file exists and is of a supported format.

    Args:
        file_path (str): Path to the file.
        supported_formats (tuple): Supported file extensions.

    Raises:
        FileNotFoundError: If the file does not exist.
        UnsupportedFileFormatError: If the file format is unsupported.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.lower().endswith(supported_formats):
        raise UnsupportedFileFormatError(f"Unsupported file format: {file_path}")
