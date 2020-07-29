import logging
import logging.config as loggingConfig
import os

from selenium import webdriver

from class_types import Logger, WebDriver


class SeleniumBase:
    RES = "Response"
    REQ = "Request"

    def __init__(self) -> None:
        self.logger = self.initialize_logger()
        self.path = os.environ.get("CHROMEDRIVER_PATH")
        self.webdriver = self.initialize_webdriver()

    def __del__(self) -> None:
        self.log("close webdriver", type=self.REQ, payload="")
        self.webdriver.quit()
        self.log("close webdriver", type=self.RES, payload="")
        self.log("close logger", type=self.REQ, payload="")
        logging.shutdown()

    def __str__(self) -> str:
        return f"Selenium base class using chromedriver at {self.path}"

    def __repr__(self) -> str:
        return f"{x.__class__.__name__}()"

    @property
    def path(self) -> str:
        self.log("get chromedriver path", type=self.REQ, payload="")
        return self.__path
        self.log("get chromedriver path", type=self.RES, payload=self.__path)

    @path.setter
    def path(self, new_path: str) -> None:
        self.log(f"set chromedriver path", type=self.REQ, payload=new_path)
        self.__path = new_path
        self.log(f"set chromedriver path", type=self.RES, payload=new_path)

    @path.deleter
    def path(self) -> None:
        self.log("reset chromedriver path", type=self.REQ, payload="")
        self.__path = ""
        self.log("reset chromedriver path", type=self.RES, payload="")

    def initialize_webdriver(self) -> WebDriver:
        self.log("initialize webdriver", type=self.REQ, payload="")
        self.webdriver = webdriver.Chrome(executable_path=self.path)
        self.log("initialize webdriver", type=self.RES, payload="")
        return self.webdriver

    def initialize_logger(self) -> Logger:
        logging_path = SeleniumBase.fetch_logging_path()
        loggingConfig.fileConfig(logging_path)
        self.logger = logging.getLogger("root")
        self.log("initialize logger", type=self.RES, payload="")
        return self.logger

    def log(self, msg: str, **kwargs: str) -> None:
        self.logger.info(msg, extra=kwargs)

    @staticmethod
    def fetch_logging_path():
        return "logging.conf"

    def process(self) -> None:
        raise ValueError


if __name__ == "__main__":
    SeleniumBase()
