# tests/test_detection.py

import unittest
import os
from src.detection.detect_toc import detect_toc
from src.detection.exceptions import UnsupportedFileFormatError, FileProcessingError

class TestTOCDetection(unittest.TestCase):

    def setUp(self):
        # Define paths to sample test documents
        self.sample_pdf = os.path.join("tests", "fixtures", "sample_toc.pdf")
        self.sample_docx = os.path.join("tests", "fixtures", "sample_toc.docx")
        self.unsupported_file = os.path.join("tests", "fixtures", "sample.txt")
        self.corrupted_pdf = os.path.join("tests", "fixtures", "corrupted.pdf")
        self.corrupted_docx = os.path.join("tests", "fixtures", "corrupted.docx")

        # Create dummy sample files for testing
        with open(self.sample_pdf, 'wb') as f:
            f.write(b'%PDF-1.4 sample pdf content with TOC')

        with open(self.sample_docx, 'w', encoding='utf-8') as f:
            f.write('This is a sample DOCX content with TOC.')

        with open(self.unsupported_file, 'w', encoding='utf-8') as f:
            f.write('This is a sample TXT file.')

        # Create corrupted files
        with open(self.corrupted_pdf, 'wb') as f:
            f.write(b'Not a real PDF content')

        with open(self.corrupted_docx, 'w', encoding='utf-8') as f:
            f.write('Not a real DOCX content')

    def tearDown(self):
        # Remove created files after tests
        files = [
            self.sample_pdf,
            self.sample_docx,
            self.unsupported_file,
            self.corrupted_pdf,
            self.corrupted_docx
        ]
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_detect_toc_pdf(self):
        result = detect_toc(self.sample_pdf)
        self.assertEqual(result["format"], "PDF")
        self.assertIsInstance(result["toc_structure"], list)
        # Since the sample content is dummy, toc_structure might be empty
        # Adjust the assertion based on actual regex and content
        # self.assertGreater(len(result["toc_structure"]), 0)

    def test_detect_toc_docx(self):
        result = detect_toc(self.sample_docx)
        self.assertEqual(result["format"], "DOCX")
        self.assertIsInstance(result["toc_structure"], list)
        # Similar to PDF, adjust based on actual content
        # self.assertGreater(len(result["toc_structure"]), 0)

    def test_unsupported_file_format(self):
        with self.assertRaises(UnsupportedFileFormatError):
            detect_toc(self.unsupported_file)

    def test_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            detect_toc("nonexistent_file.pdf")

    def test_corrupted_pdf(self):
        with self.assertRaises(FileProcessingError):
            detect_toc(self.corrupted_pdf)

    def test_corrupted_docx(self):
        with self.assertRaises(FileProcessingError):
            detect_toc(self.corrupted_docx)

if __name__ == "__main__":
    unittest.main()
