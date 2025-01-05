# src/detection/detect_toc.py

import os
import re
import logging
from PyPDF2 import PdfReader
from docx import Document
from .config import (
    PROJECT_ROOT,
    SUPPORTED_FORMATS,
    PDF_TOC_REGEX,
    DOCX_TOC_REGEX
)
from .exceptions import (
    TOCDetectionError,
    UnsupportedFileFormatError,
    FileProcessingError
)
from .utils import validate_file_path

def detect_toc(file_path):
    """
    Detects a Table of Contents (TOC) in a document.

    Args:
        file_path (str): Path to the document.

    Returns:
        dict: Detected TOC structure and metadata.
    """
    logging.info(f"Starting TOC detection for file: {file_path}")
    try:
        validate_file_path(file_path, SUPPORTED_FORMATS)
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            result = detect_toc_pdf(file_path)
        elif ext == ".docx":
            result = detect_toc_docx(file_path)
        else:
            raise UnsupportedFileFormatError("Only PDF and DOCX formats are supported.")
        logging.info(f"TOC detection completed successfully for {file_path}")
        return result
    except TOCDetectionError as e:
        logging.error(f"TOCDetectionError: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error during TOC detection for {file_path}: {e}")
        raise FileProcessingError(f"Failed to process {file_path}") from e

def detect_toc_pdf(file_path):
    """Detects TOC patterns in a PDF file."""
    toc_structure = []
    try:
        reader = PdfReader(file_path)
        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if text:
                matches = re.findall(PDF_TOC_REGEX, text)
                # Flatten the matches if regex has groups
                flat_matches = [".".join(filter(None, match)).strip() for match in matches]
                toc_structure.extend(flat_matches)
            else:
                logging.warning(f"No text found on page {page_number} of {file_path}")
        return {"format": "PDF", "toc_structure": toc_structure}
    except Exception as e:
        logging.error(f"Error processing PDF file {file_path}: {e}")
        raise FileProcessingError(f"Error processing PDF file {file_path}") from e

def detect_toc_docx(file_path):
    """Detects TOC patterns in a DOCX file."""
    toc_structure = []
    try:
        doc = Document(file_path)
        for para_number, paragraph in enumerate(doc.paragraphs, start=1):
            matches = re.findall(DOCX_TOC_REGEX, paragraph.text)
            flat_matches = [".".join(filter(None, match)).strip() for match in matches]
            toc_structure.extend(flat_matches)
        return {"format": "DOCX", "toc_structure": toc_structure}
    except Exception as e:
        logging.error(f"Error processing DOCX file {file_path}: {e}")
        raise FileProcessingError(f"Error processing DOCX file {file_path}") from e
