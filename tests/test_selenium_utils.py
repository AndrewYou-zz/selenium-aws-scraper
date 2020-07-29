from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from scraper import Scraper
from selenium_utils import ElementHasCssSelector


def test_elements_found():
    obj = Scraper("https://www.google.com/", "bar.csv", ["foo1", "foo2", "foo3"], True)
    obj.go_to(obj.base_url)
    elements = WebDriverWait(obj.webdriver, 3).until(
        ElementHasCssSelector("input[value*= 'Feeling Lucky']")
    )
    assert elements


def test_no_elements_found():
    obj = Scraper("https://www.google.com/", "bar.csv", ["foo1", "foo2", "foo3"], True)
    obj.go_to(obj.base_url)
    try:
        elements = WebDriverWait(obj.webdriver, 3).until(
            ElementHasCssSelector("input[value*= 'Not Feeling Lucky']")
        )
    except TimeoutException:
        pass
