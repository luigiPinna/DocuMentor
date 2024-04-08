from setup import Setup
from logger import Logger
import openai
from pdfManager import PDFManager

# Setup
my_setup = Setup()

# Logger
my_logger = Logger('DocuMentorLogger', log_file=my_setup.main_log_file_path).get_logger()

my_logger.info("Starting DocuMentor...")

openai.api_key = my_setup.openai_api_key

# pdf manager
pdf_manager = PDFManager(my_setup.regolamento_file_path)

print(pdf_manager.read_text())
