import logging
import logging.config as loggingConfig
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

    def initialize_webdriver(self) -> webdriver:
        self.log('Initializing webdriver.')
        self.webdriver = webdriver.Chrome(executable_path=self.path)
        self.log('Initialized webdriver.')
        return self.webdriver

    def initialize_logger(self) -> logging.Logger:
        loggingConfig.fileConfig('logging.conf')
        self.logger = logging.getLogger('root')
        self.log('Initialized logger.')
        return self.logger

    def log(self, msg: str) -> None:
        self.logger.info(msg)

    def process(self) -> None:
        pass

if __name__ == '__main__':
    SeleniumBase().process()