# Rag Project V2

This is the main project README.

# TOC Detection Module

## Overview

This module detects Tables of Contents (TOC) in PDF and DOCX documents. It extracts the TOC structure and saves the results in JSON format.

## Project Structure

Rag Project V2/ ├── src/ │ ├── detection/ │ │ ├── config.py │ │ ├── detect_toc.py │ │ ├── exceptions.py │ │ └── utils.py │ ├── scripts/ │ │ └── process_tocs.py │ └── utils/ │ └── git_utils.py ├── tests/ │ └── test_detection.py ├── data/ │ ├── processed_data/ │ └── sample_documents/ ├── logs/ │ └── performance_logs/ ├── deployment/ ├── ci_cd/ ├── requirements.txt └── README.md


## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/rag-project-v2.git
   cd rag-project-v2
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

3. **Install Dependencies:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Prepare Sample Documents:**

   Place your PDF and DOCX files in the `data/sample_documents/` directory.

5. **Run TOC Detection Script:**

   ```bash
   python src/scripts/process_tocs.py
   ```

   This script will process all supported files in the sample documents directory, extract TOC structures, save the results to `data/processed_data/detected_tocs.json`, and commit the changes to Git.

## Running Tests

Ensure you have the necessary test fixtures in the `tests/fixtures/` directory.

```bash
python -m unittest discover tests

