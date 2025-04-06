import os
import sys
from configparser import ConfigParser


class Setup:
    def __init__(self):
        # Identifica esplicitamente la directory DocuMentor dal percorso di esecuzione
        script_path = os.path.abspath(sys.argv[0])
        # Estrai "DocuMentor" dal percorso completo
        path_parts = script_path.split(os.sep)

        # Trova l'indice di "DocuMentor" nel percorso
        project_index = -1
        for i, part in enumerate(path_parts):
            if part == "DocuMentor":
                project_index = i
                break

        # Se "DocuMentor" è stato trovato nel percorso
        if project_index >= 0:
            # Costruisci il percorso fino a includere "DocuMentor"
            self.base_dir = os.sep.join(path_parts[:project_index + 1])
        else:
            # Fallback: usa il percorso corrente e avvisa
            self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            print(f"ATTENZIONE: Non è stato possibile determinare con certezza la directory del progetto DocuMentor.")

        setup = ConfigParser()

        # Percorsi possibili per il file di configurazione
        config_paths = [
            os.path.join(self.base_dir, 'config.ini'),
            os.path.join(self.base_dir, 'app', 'config.ini'),
            'config.ini',
            '../config.ini'
        ]

        # Cerca il file di configurazione nei percorsi possibili
        config_file = None
        for path in config_paths:
            if os.path.isfile(path):
                config_file = path
                break

        # Se non è stato trovato, solleva un'eccezione
        if not config_file:
            raise FileNotFoundError(f"File di configurazione non trovato nei percorsi: {', '.join(config_paths)}")

        # Leggi il file di configurazione
        setup.read(config_file)

        # File paths - sempre relativi alla directory del progetto
        input_kb_folder = setup.get("FILE", "input_kb_folder")
        main_log_file_path = setup.get("FILE", "main_log_file_path")

        # Converti sempre i percorsi relativi alla directory del progetto
        self.input_kb_folder = os.path.join(self.base_dir, input_kb_folder)
        self.main_log_file_path = os.path.join(self.base_dir, main_log_file_path)

        # Crea le directory per i log e i dati
        os.makedirs(os.path.dirname(self.main_log_file_path), exist_ok=True)
        os.makedirs(self.input_kb_folder, exist_ok=True)

        # Debug info
        print(f"Directory dei dati: {self.input_kb_folder}")
        print(f"File di log: {self.main_log_file_path}")

        # AI
        self.openai_api_key = setup.get("AI", "openai_api_key")