import sys
import os
import re
import logging
from PyPDF2 import PdfReader
from docx import Document
from src.utils.git_utils import auto_commit_push

# Add the root directory to sys.path
current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(os.path.dirname(current_file), "../../"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    filename=os.path.join(project_root, "logs", "detection_errors.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
        if file_path.endswith(".pdf"):
            result = detect_toc_pdf(file_path)
        elif file_path.endswith(".docx"):
            result = detect_toc_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
        logging.info(f"TOC detection completed successfully: {result}")
        return result
    except Exception as e:
        logging.error(f"Error during TOC detection: {e}")
        raise

def detect_toc_pdf(file_path):
    """Detects TOC patterns in a PDF file."""
    reader = PdfReader(file_path)
    toc_structure = []
    for page in reader.pages:
        text = page.extract_text()
        matches = re.findall(r"\d+\.\s+\w+", text)
        toc_structure.extend(matches)
    return {"format": "PDF", "toc_structure": toc_structure}

def detect_toc_docx(file_path):
    """Detects TOC patterns in a DOCX file."""
    doc = Document(file_path)
    toc_structure = []
    for paragraph in doc.paragraphs:
        if match := re.search(r"\d+\.\s+\w+", paragraph.text):
            toc_structure.append(match.group())
    return {"format": "DOCX", "toc_structure": toc_structure}

if __name__ == "__main__":
    # Define the directory containing sample documents
    sample_dir = os.path.join(project_root, "data", "sample_documents")

    # Ensure the directory exists
    if not os.path.exists(sample_dir):
        print(f"Sample directory not found: {sample_dir}")
        exit(1)

    # List all PDF and DOCX files in the directory
    files_to_process = [
        os.path.join(sample_dir, file)
        for file in os.listdir(sample_dir)
        if file.endswith((".pdf", ".docx"))
    ]

    if not files_to_process:
        print(f"No PDF or DOCX files found in: {sample_dir}")
        exit(1)

    # Process each file
    for file_path in files_to_process:
        print(f"Processing file: {file_path}")
        try:
            result = detect_toc(file_path)
            print(f"Result for {file_path}:\n{result}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Commit and push changes to GitHub
    auto_commit_push("Processed multiple sample files for TOC detection")
