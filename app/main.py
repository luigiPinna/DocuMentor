from setup import Setup
from logger import Logger
import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import sys

# Initialize Logger
try:
    my_setup = Setup()
    my_logger = Logger('DocuMentorLogger', log_file=my_setup.main_log_file_path).get_logger()
    my_logger.info("DocuMentor starting...")
except Exception as e:
    print(f"Error during initial setup: {e}")
    sys.exit(1)

# Set openAi APi key
my_logger.info("Setting up OpenAI API key...")
try:
    openai.api_key = my_setup.openai_api_key
    my_logger.info("OpenAI API key set successfully.")
except Exception as e:
    my_logger.error(f"Failed to set OpenAI API key: {e}")
    sys.exit(1)

# Load documents
my_logger.info("Loading documents and creating index...")
try:
    documents = SimpleDirectoryReader(my_setup.input_kb_folder).load_data()
    # Index creation
    index = VectorStoreIndex.from_documents(documents)
    my_logger.info("Documents loaded and index created successfully.")
except Exception as e:
    if "insufficient_quota" in str(e):
        my_logger.error("Quota limit exceeded: Please check your plan and billing details.")
    else:
        my_logger.error(f"Error loading documents or creating index: {e}")
    sys.exit(1)

my_logger.info("Performing a query on the index...")

# Request a question from the user
question = input("Please enter your question: ")
my_logger.info(f"Received question: {question}")

# Engine and push the query with question
try:
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    print(response)
    my_logger.info(f"Query response: {response}")
except Exception as e:
    my_logger.error(f"Error executing query: {e}")
    sys.exit(1)
