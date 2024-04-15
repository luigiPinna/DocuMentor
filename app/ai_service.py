import openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
import sys


class AIService:
    def __init__(self, logger, setup):
        """
        Initializes the AI service by setting the OpenAI API key and loading documents to create an index.

        Args:
            logger: The logger object for logging messages.
            setup: The setup configuration object containing settings and API keys.

        The constructor will terminate the program if setting the API key or loading documents fails.
        """
        self.logger = logger
        self.setup = setup
        self.index = None
        self.query_engine = None

        # Set OpenAI API key
        self.set_api_key()

        # Load documents and create index
        self.load_documents_and_create_index()

    def set_api_key(self):
        """Sets the OpenAI API key from the setup configuration."""
        self.logger.info("Setting up OpenAI API key...")
        try:
            openai.api_key = self.setup.openai_api_key
            self.logger.info("OpenAI API key set successfully.")
        except Exception as e:
            self.logger.error(f"Failed to set OpenAI API key: {e}")

    def load_documents_and_create_index(self):
        """Loads documents from the specified directory and creates an index for querying.

        Logs the process and handles exceptions by logging errors and exiting the program if an error occurs.
        Specifically handles 'insufficient_quota' errors by logging a message about quota limits.
        """
        self.logger.info("Loading documents and creating index...")
        try:
            documents = SimpleDirectoryReader(self.setup.input_kb_folder).load_data()
            self.index = VectorStoreIndex.from_documents(documents)
            self.query_engine = self.index.as_query_engine()
            self.logger.info("Documents loaded and index created successfully.")
        except Exception as e:
            if "insufficient_quota" in str(e):
                self.logger.error("Quota limit exceeded: Please check your plan and billing details.")
            else:
                self.logger.error(f"Error loading documents or creating index: {e}")

    def perform_query(self, question):
        """Performs a query against the loaded documents using the provided question.

        Args:
            question: The user's question to query against the document index.

        Returns:
            The response from the query engine.
"""
        self.logger.info("Performing a query on the index...")
        try:
            response = self.query_engine.query(question)
            self.logger.info(f"Query response: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
