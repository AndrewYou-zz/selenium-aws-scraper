from typing import List

import selenium
from selenium import webdriver
import logging

WebDriver = webdriver
WebElements = List[WebDriver.remote.webelement.WebElement]

Logger = logging.Logger
