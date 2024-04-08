import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name, log_file='app.log', level=logging.INFO):
        """
        Logger Initialization

        :param name: Text.
        :param log_file: Log file path.
        :param level: Log level.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # msg format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Handler output a console
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # make dir if the folder doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # file configs
        fh = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def get_logger(self):
        """
        Returns logger instance
        """
        return self.logger
