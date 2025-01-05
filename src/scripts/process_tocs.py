# src/scripts/process_tocs.py

import os
import sys
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.detection.detect_toc import detect_toc
from src.utils.git_utils import auto_commit_push
from src.detection.utils import setup_logging
from src.detection.config import (
    PROJECT_ROOT,
    SAMPLE_DOCUMENTS_DIR,
    GIT_COMMIT_MESSAGE
)

def main():
    # Set up logging
    setup_logging()
    
    # Define the directory containing sample documents
    sample_dir = SAMPLE_DOCUMENTS_DIR

    # Ensure the directory exists
    if not os.path.exists(sample_dir):
        logging.error(f"Sample directory not found: {sample_dir}")
        sys.exit(1)

    # List all PDF and DOCX files in the directory
    files_to_process = [
        os.path.join(sample_dir, file)
        for file in os.listdir(sample_dir)
        if file.lower().endswith((".pdf", ".docx"))
    ]

    if not files_to_process:
        logging.warning(f"No PDF or DOCX files found in: {sample_dir}")
        sys.exit(0)

    logging.info(f"Found {len(files_to_process)} files to process.")

    # Prepare a list to hold results
    results = []

    def process_file(file_path):
        """Processes a single file and returns the result."""
        try:
            result = detect_toc(file_path)
            logging.info(f"Successfully processed {file_path}")
            return (file_path, result, None)
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            return (file_path, None, str(e))

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {executor.submit(process_file, fp): fp for fp in files_to_process}
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                fp, res, err = future.result()
                if res:
                    results.append(res)
                if err:
                    logging.error(f"Failed to process {fp}: {err}")
            except Exception as e:
                logging.error(f"Unhandled exception processing {file_path}: {e}")

    # Save results to JSON
    import json
    processed_data_dir = os.path.join(PROJECT_ROOT, "data", "processed_data")
    os.makedirs(processed_data_dir, exist_ok=True)
    detected_tocs_file = os.path.join(processed_data_dir, "detected_tocs.json")
    with open(detected_tocs_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    logging.info(f"TOC detection results saved to {detected_tocs_file}")

    # Commit and push changes to GitHub
    try:
        auto_commit_push(GIT_COMMIT_MESSAGE)
    except Exception as e:
        logging.error(f"Git commit and push failed: {e}")

if __name__ == "__main__":
    main()
