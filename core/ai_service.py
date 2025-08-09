import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai import OpenAI
from typing import Optional

from core.logging import logger


class AIService:
    """Servizio per gestire le operazioni AI e RAG"""

    def __init__(self, config_manager):
        """
        Inizializza il servizio AI configurando l'API key e caricando i documenti.

        Args:
            config_manager: ConfigManager per le configurazioni
        """
        self.config_manager = config_manager
        self.index: Optional[VectorStoreIndex] = None
        self.query_engine = None

        # Configura l'ambiente AI
        self._setup_ai_environment()

        # Carica documenti e crea l'indice
        self._load_documents_and_create_index()

    def _setup_ai_environment(self) -> None:
        """Configura l'ambiente AI con API key e modello"""
        logger.info("Configurazione ambiente AI...")

        try:
            os.environ["OPENAI_API_KEY"] = self.config_manager.openai_api_key

            # Configura LlamaIndex
            Settings.llm = OpenAI(
                model=self.config_manager.ai_model,
                temperature=self.config_manager.ai_temperature
            )

            logger.info(f"Ambiente AI configurato - Modello: {self.config_manager.ai_model}")

        except Exception as e:
            logger.error(f"Errore nella configurazione AI: {e}")
            raise

    def _load_documents_and_create_index(self) -> None:
        """Carica i documenti dalla directory specificata e crea l'indice per le query"""
        logger.info("Caricamento documenti e creazione indice...")

        try:
            # Verifica che la directory esista
            if not self.config_manager.input_kb_folder.exists():
                error_msg = f"Directory non trovata: {self.config_manager.input_kb_folder}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)

            # Verifica che ci siano file nella directory
            files = list(self.config_manager.input_kb_folder.glob("*"))
            files = [f for f in files if f.is_file()]

            if not files:
                error_msg = f"Nessun file trovato in {self.config_manager.input_kb_folder}"
                logger.error(error_msg)
                raise FileNotFoundError(error_msg)

            logger.info(f"File trovati: {[f.name for f in files]}")

            # Carica i documenti
            documents = SimpleDirectoryReader(
                str(self.config_manager.input_kb_folder)
            ).load_data()

            if not documents:
                error_msg = "Nessun documento valido caricato"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Crea l'indice
            self.index = VectorStoreIndex.from_documents(documents)
            self.query_engine = self.index.as_query_engine()

            logger.info(f"Indice creato con successo - {len(documents)} documenti processati")

        except Exception as e:
            error_msg = f"Errore durante il caricamento documenti: {e}"
            logger.error(error_msg)

            # Gestione specifica per errori di quota OpenAI
            if "insufficient_quota" in str(e).lower():
                logger.error("Quota OpenAI esaurita - Verifica il piano e la fatturazione")

            raise

    def perform_query(self, question: str) -> str:
        """
        Esegue una query sui documenti caricati.

        Args:
            question: Domanda dell'utente

        Returns:
            Risposta del sistema AI

        Raises:
            ValueError: Se l'indice non è stato creato correttamente
            Exception: Per altri errori durante l'esecuzione della query
        """
        if not question or not question.strip():
            raise ValueError("La domanda non può essere vuota")

        logger.info(f"Esecuzione query: {question[:100]}...")

        try:
            # Verifica che l'indice sia stato creato
            if self.query_engine is None:
                error_msg = "Impossibile eseguire la query: indice non inizializzato"
                logger.error(error_msg)
                raise ValueError(error_msg)

            # Esegui la query
            response = self.query_engine.query(question)

            logger.info("Query eseguita con successo")
            return str(response)

        except Exception as e:
            error_msg = f"Errore durante l'esecuzione della query: {e}"
            logger.error(error_msg)
            raise