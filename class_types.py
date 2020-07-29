import logging
from typing import Dict, List

import selenium
from selenium import webdriver

# Selenium Types
WebDriver = webdriver
WebElements = List[WebDriver.remote.webelement.WebElement]

# Logging Types
Logger = logging.Logger

# Vector Types
VectorString = List[str]
VectorDict = List[Dict]
