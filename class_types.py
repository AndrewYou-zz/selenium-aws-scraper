import logging
from typing import Dict, List

import selenium
from selenium import webdriver

WebDriver = webdriver
WebElements = List[WebDriver.remote.webelement.WebElement]

Logger = logging.Logger

VectorString = List[str]
VectorDict = List[Dict]
