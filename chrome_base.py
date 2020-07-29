import logging
import logging.config as loggingConfig
import os
from abc import ABC, abstractmethod

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from class_types import Logger, WebDriver


class ChromedriverBase(ABC):
    RES = "Response"
    REQ = "Request"

    def __init__(self, headless: bool) -> None:
        self.logger = self.initialize_logger()
        self.path = ChromedriverBase.fetch_chromedriver_path()
        self.webdriver = self.initialize_webdriver(headless)

    def __del__(self) -> None:
        """ Closes logging and webdriver when reference count reaches 0 """
        self.log("close webdriver", type=self.REQ, payload="")
        try:
            self.webdriver.quit()
        except ImportError as e:
            if e == "sys.meta_path is None, Python is likely shutting down":
                pass
        self.log("close webdriver", type=self.RES, payload="")
        self.log("close logger", type=self.REQ, payload="")
        logging.shutdown()

    def __str__(self) -> str:
        return f"Using chromedriver at {self.path}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    @property
    def path(self) -> str:
        """ Get interface for __path private variable """
        self.log("get chromedriver path", type=self.REQ, payload="")
        return self.__path
        self.log("get chromedriver path", type=self.RES, payload=self.__path)

    @path.setter
    def path(self, new_path: str) -> None:
        """ Set interface for __path private variable """
        self.log(f"set chromedriver path", type=self.REQ, payload=new_path)
        self.__path = new_path
        self.log(f"set chromedriver path", type=self.RES, payload=new_path)

    @path.deleter
    def path(self) -> None:
        """ Delete interface for __path private variable """
        self.log("reset chromedriver path", type=self.REQ, payload="")
        self.__path = ""
        self.log("reset chromedriver path", type=self.RES, payload="")

    def initialize_webdriver(self, headless: bool) -> WebDriver:
        """ Initializes chromedriver """
        self.log("initialize webdriver", type=self.REQ, payload=f"{headless!r}")
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        self.webdriver = webdriver.Chrome(
            executable_path=self.path, chrome_options=chrome_options
        )
        self.log("initialize webdriver", type=self.RES, payload="")
        return self.webdriver

    def initialize_logger(self) -> Logger:
        """ Initializes logging """
        logging_path = ChromedriverBase.fetch_logging_path()
        loggingConfig.fileConfig(logging_path)
        self.logger = logging.getLogger("root")
        self.log("initialize logger", type=self.RES, payload="")
        return self.logger

    def log(self, msg: str, **kwargs: str) -> None:
        """ Logs to stdout """
        self.logger.info(msg, extra=kwargs)

    @staticmethod
    def fetch_logging_path() -> str:
        """ Fetches path to logging.conf """
        return "config/logging.conf"

    @staticmethod
    def fetch_chromedriver_path() -> str:
        """ Fetches path to chromedriver """
        return os.environ.get("CHROMEDRIVER_PATH")

    @abstractmethod
    def process(self) -> None:
        """ Contains main business logic for scraping website (must be implemented) """
        pass
