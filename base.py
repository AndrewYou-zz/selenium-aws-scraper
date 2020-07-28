import logging
import logging.config as loggingConfig
from class_types import WebDriver, Logger

import os
from selenium import webdriver


class SeleniumBase:
    def __init__(self) -> None:
        self.logger = self.initialize_logger()
        self.path = os.environ.get('CHROMEDRIVER_PATH')
        self.webdriver = self.initialize_webdriver()

    def __del__(self) -> None:
        self.webdriver.quit()
        self.log('Closed webdriver.')
        self.log('Closing logging.')
        logging.shutdown()

    def __str__(self) -> str:
        return f"Selenium base class using chromedriver at {self.path}"

    def __repr__(self) -> str:
        return f"{x.__class__.__name__}()"

    @property
    def path(self) -> str:
        self.log('Getting chromedriver path.')
        return self.__path

    @path.setter
    def path(self, new_path: str) -> None:
        self.log(f'Setting chromedriver path to {new_path}.')
        self.__path = new_path

    @path.deleter
    def path(self) -> None:
        self.log('Resetting chromedriver path.')
        self.__path = ''

    def initialize_webdriver(self) -> WebDriver:
        self.log('Initializing webdriver.')
        self.webdriver = webdriver.Chrome(executable_path=self.path)
        self.log('Initialized webdriver.')
        return self.webdriver

    def initialize_logger(self) -> Logger:
        logging_path = SeleniumBase.fetch_logging_path()
        loggingConfig.fileConfig(logging_path)
        self.logger = logging.getLogger('root')
        self.log('Initialized logger.')
        return self.logger

    def log(self, msg: str) -> None:
        self.logger.info(msg)

    @staticmethod
    def fetch_logging_path():
        return 'logging.conf'

    def process(self) -> None:
        raise ValueError
