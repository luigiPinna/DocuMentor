import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Union, Optional


class LoggingManager:
    """Singleton per gestire il logging dell'applicazione"""

    _instance: Optional['LoggingManager'] = None
    _initialized: bool = False

    def __new__(cls) -> 'LoggingManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Evita reinizializzazione multipla
        if LoggingManager._initialized:
            return
        LoggingManager._initialized = True

        self._logger: Optional[logging.Logger] = None

    def initialize(self, name: str = 'DocuMentor', log_file: Union[str, Path] = 'app.log',
                   level: int = logging.INFO) -> None:
        """
        Inizializza il logger (da chiamare una sola volta all'avvio)

        Args:
            name: Nome del logger
            log_file: Percorso del file di log
            level: Livello di logging
        """
        if self._logger is not None:
            return  # Già inizializzato

        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)

        # Evita handler duplicati
        if self._logger.handlers:
            return

        # Converte il log_file in Path se è una stringa
        log_file_path = Path(log_file)

        # Formato dei messaggi
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler per output su console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self._logger.addHandler(console_handler)

        # Crea la directory del log se non esiste
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Handler per file con rotazione
        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=1024 * 1024 * 5,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Restituisce l'istanza del logger"""
        if self._logger is None:
            raise RuntimeError("Logger non inizializzato. Chiamare initialize() prima dell'uso.")
        return self._logger

    # Metodi di convenience per logging diretto
    def debug(self, message: str) -> None:
        self.get_logger().debug(message)

    def info(self, message: str) -> None:
        self.get_logger().info(message)

    def warning(self, message: str) -> None:
        self.get_logger().warning(message)

    def error(self, message: str) -> None:
        self.get_logger().error(message)

    def critical(self, message: str) -> None:
        self.get_logger().critical(message)


# Istanza globale singleton
logger = LoggingManager()