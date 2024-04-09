from PyPDF2 import PdfReader


class PDFManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_text(self):
        """Get all pdf text from file and returns the text as a string"""
        text = ''
        pdf_reader = PdfReader(self.file_path)
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
