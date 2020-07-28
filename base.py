import logging
import logging.config as loggingConfig
from selenium import webdriver

class SeleniumBase:

    def __init__(self) -> None:
        self.logger = self.initialize_logger()
        self.webdriver = webdriver.Chrome(executable_path='/Users/andrewyou/Desktop/selenium-aws-webscraper/chromedriver')

    def __del__(self) -> None:
        self.webdriver.quit()
        self.log('Closed webdriver.')

    def initialize_logger(self) -> logging.Logger:
        loggingConfig.fileConfig('logging.conf')
        self.logger = logging.getLogger('root')
        self.log('Instantiated logger.')
        return self.logger

    def log(self, msg: str) -> None:
        self.logger.info(msg)

    def process(self) -> None:
        pass

if __name__ == '__main__':
    SeleniumBase().process()