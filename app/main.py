from setup import Setup
from logger import Logger

# Setup
my_setup = Setup()

# Logger
my_logger = Logger('DocuMentorLogger', log_file=my_setup.main_log_file_path).get_logger()

my_logger.info("Starting DocuMentor...")

