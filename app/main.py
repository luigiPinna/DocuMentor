from setup import Setup
from logger import Logger
from ai_service import AIService
import sys


def main():
    # Logger and Setup init
    try:
        my_setup = Setup()
        my_logger = Logger('DocuMentorLogger', log_file=my_setup.main_log_file_path).get_logger()
        my_logger.info("DocuMentor starting...")
    except Exception as e:
        print(f"Error during initial setup: {e}")
        sys.exit(1)
    # AIService instance
    ai_service = AIService(my_logger, my_setup)

    # User question
    question = input("Please enter your question: ")
    my_logger.info(f"Received question: {question}")

    # Query execution
    response = ai_service.perform_query(question)
    print(response)


if __name__ == "__main__":
    main()
