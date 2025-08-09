import os
from pathlib import Path
from configparser import ConfigParser
from dotenv import load_dotenv


class ConfigManager:
    """Gestisce la configurazione dell'applicazione"""

    def __init__(self, config_file: str = "config/config.ini"):
        # Carica le variabili d'ambiente
        load_dotenv()

        # Carica la configurazione
        self.config = self._load_config(config_file)

        # Inizializza i percorsi
        self._setup_paths()

        # Crea le directory necessarie
        self._create_directories()

    def _load_config(self, config_file: str) -> ConfigParser:
        """Carica la configurazione dal file INI"""
        config_path = Path(config_file)

        if not config_path.exists():
            raise FileNotFoundError(
                f"File di configurazione non trovato: {config_file}\n"
                f"Assicurati che il file esista nella directory corrente."
            )

        config = ConfigParser()
        try:
            config.read(config_path, encoding='utf-8')
            return config
        except Exception as e:
            raise ValueError(f"Errore nel parsing del file INI: {e}")

    def _setup_paths(self) -> None:
        """Configura tutti i percorsi dell'applicazione"""
        # Percorsi dalla configurazione (relativi alla directory corrente)
        input_kb_folder = self.config.get("FILE", "input_kb_folder", fallback="data")
        log_folder = self.config.get("FILE", "log_folder", fallback="logs")
        main_log_file = self.config.get("FILE", "main_log_file", fallback="app.log")

        # Converte in Path objects
        self.input_kb_folder = Path(input_kb_folder)
        self.log_folder = Path(log_folder)
        self.main_log_file_path = self.log_folder / main_log_file

    def _create_directories(self) -> None:
        """Crea le directory necessarie se non esistono"""
        directories = [self.input_kb_folder, self.log_folder]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    @property
    def openai_api_key(self) -> str:
        """Restituisce la chiave API di OpenAI dalle variabili d'ambiente"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY non trovata nelle variabili d'ambiente.\n"
                "Assicurati di aver creato un file .env con OPENAI_API_KEY=la_tua_chiave"
            )
        return api_key

    @property
    def ai_model(self) -> str:
        """Restituisce il modello AI da utilizzare"""
        return self.config.get("AI", "model", fallback="gpt-3.5-turbo")

    @property
    def ai_temperature(self) -> float:
        """Restituisce la temperatura per il modello AI"""
        return self.config.getfloat("AI", "temperature", fallback=0.7)

    def get_config_value(self, section: str, key: str, fallback=None):
        """Metodo generico per ottenere valori dalla configurazione"""
        return self.config.get(section, key, fallback=fallback)