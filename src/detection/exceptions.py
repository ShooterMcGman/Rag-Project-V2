# src/detection/exceptions.py

class TOCDetectionError(Exception):
    """Base exception for TOC detection errors."""
    pass

class UnsupportedFileFormatError(TOCDetectionError):
    """Exception raised for unsupported file formats."""
    pass

class FileProcessingError(TOCDetectionError):
    """Exception raised when file processing fails."""
    pass
