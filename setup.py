import os
from configparser import ConfigParser


class Setup:
    def __init__(self):
        setup = ConfigParser()
        yaml_setup_file = 'config.yml'
        if not os.path.isfile(yaml_setup_file):
            yaml_setup_file = '../config.yml'
        setup.read(yaml_setup_file)
        # File paths
        self.input_kb_folder = setup.get("FILE", "input_kb_folder")
        self.main_log_file_path = setup.get("FILE", "main_log_file_path")