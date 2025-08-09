import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Union


class Logger:
    """Gestisce il logging dell'applicazione con supporto per Path objects"""

    def __init__(self, name: str, log_file: Union[str, Path] = 'app.log', level: int = logging.INFO):
        """
        Inizializzazione del Logger

        Args:
            name: Nome del logger
            log_file: Percorso del file di log (str o Path)
            level: Livello di logging
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Converte il log_file in Path se è una stringa
        self.log_file_path = Path(log_file)

        # Formato dei messaggi
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler per output su console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Crea la directory del log se non esiste
        self.log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Handler per file con rotazione
        file_handler = RotatingFileHandler(
            self.log_file_path,
            maxBytes=1024 * 1024 * 5,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Restituisce l'istanza del logger"""
        return self.logger