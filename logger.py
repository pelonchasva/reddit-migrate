import logging
import os, sys
from datetime import datetime

class Logger(object):
    """
    Logger class that writes the messages to a file
    """

    def __init__(self, name: str):
        """
        """
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.f_handler = logging.FileHandler(self.get_log_file())
        self.f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.f_handler.setFormatter(self.f_format)
        self.logger.addHandler(self.f_handler)

    def debug(self, msg: str):
        """
        """
        self.logger.setLevel(logging.DEBUG)
        self.logger.debug(msg)

    def info(self, msg: str):
        """
        """
        self.logger.setLevel(logging.INFO)
        self.logger.info(msg)

    def warn(self, msg: str):
        """
        """
        self.logger.setLevel(logging.WARN)
        self.logger.warn(msg)

    def error(self, ex: Exception, msg: str):
        """
        """
        self.logger.setLevel(logging.ERROR)
        self.logger.error(ex)
        self.logger.error(msg)

    def critical(self, ex: Exception, msg: str):
        """
        """
        self.logger.setLevel(logging.CRITICAL)
        self.logger.critical(ex)
        self.logger.critical(msg)

    def get_log_file(self, path="./log/Reddit-Migrate.log"):
        """
        Returns the path of the log file or creates one if needed
        """
        # Check if log folders exists, otherwise create it
        if not os.path.exists('./log'):
            try:
                os.mkdir('./log')
            except OSError as ex:
                print(f"Could not create folder './log'.")

        if not os.path.exists(path):
            with open(path, "w+") as f:
                log_date = datetime.today()
                f.write("===== Log File Created on: {0} =====\n".format(log_date))
            print("Log file created.")

        return path
