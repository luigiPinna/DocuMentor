import os
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

        # Set OpenAI API key using environment variable
        self.set_api_key()

        # Load documents and create index
        self.load_documents_and_create_index()

    def set_api_key(self):
        """Sets the OpenAI API key from the setup configuration."""
        self.logger.info("Setting up OpenAI API key...")
        try:
            # Set API key as environment variable instead of using the client directly
            os.environ["OPENAI_API_KEY"] = self.setup.openai_api_key
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
            # Check if the directory exists and has files
            if not os.path.exists(self.setup.input_kb_folder):
                self.logger.error(f"Directory does not exist: {self.setup.input_kb_folder}")
                return

            files = [f for f in os.listdir(self.setup.input_kb_folder)
                     if os.path.isfile(os.path.join(self.setup.input_kb_folder, f))]

            if not files:
                self.logger.error(f"No files found in {self.setup.input_kb_folder}")
                return

            self.logger.info(f"Found files: {', '.join(files)}")

            # Load documents
            documents = SimpleDirectoryReader(self.setup.input_kb_folder).load_data()

            # Try to create index - use catch blocks to handle failures
            try:
                # Try alternative way to initialize the index
                from llama_index.core import Settings
                from llama_index.llms.openai import OpenAI

                # Configure settings explicitly to avoid proxies issue
                Settings.llm = OpenAI(model="gpt-3.5-turbo")

                self.index = VectorStoreIndex.from_documents(documents)
                self.query_engine = self.index.as_query_engine()
                self.logger.info("Documents loaded and index created successfully.")
            except Exception as e:
                self.logger.error(f"Error creating index with settings: {e}")
                # Fallback to direct creation
                try:
                    self.index = VectorStoreIndex.from_documents(documents)
                    self.query_engine = self.index.as_query_engine()
                    self.logger.info("Documents loaded and index created successfully (fallback).")
                except Exception as inner_e:
                    self.logger.error(f"Error creating index (fallback): {inner_e}")

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
            The response from the query engine or error message.
        """
        self.logger.info("Performing a query on the index...")
        try:
            # Check if index was properly created
            if self.query_engine is None:
                error_msg = "Unable to answer query because the document index was not properly created."
                self.logger.error(error_msg)
                return error_msg

            response = self.query_engine.query(question)
            self.logger.info("Query executed successfully")
            return response
        except Exception as e:
            error_msg = f"Error executing query: {e}"
            self.logger.error(error_msg)
            return f"Sorry, I encountered an error: {e}"