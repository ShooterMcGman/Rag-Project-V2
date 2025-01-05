# src/detection/config.py

import os

# Project Root Directory
CURRENT_FILE = os.path.abspath(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(CURRENT_FILE), "../../"))

# Data Directories
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw_data")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed_data")
SAMPLE_DOCUMENTS_DIR = os.path.join(DATA_DIR, "sample_documents")

# Logs Configuration
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
DETECTION_LOG_FILE = os.path.join(LOG_DIR, "detection_errors.log")
PERFORMANCE_LOG_FILE = os.path.join(LOG_DIR, "performance_logs", "performance_metrics.log")

# Supported File Formats
SUPPORTED_FORMATS = (".pdf", ".docx")

# TOC Detection Regex Patterns
PDF_TOC_REGEX = r"\d+(\.\d+)*\s+[\w\s]+(\.\.\.\d+)?"
DOCX_TOC_REGEX = r"\d+(\.\d+)*\s+[\w\s]+(\.\.\.\d+)?"

# Logging Settings
LOGGING_LEVEL = "INFO"
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Git Commit Message
GIT_COMMIT_MESSAGE = "Processed multiple sample files for TOC detection"
