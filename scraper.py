from base import SeleniumBase
from selenium_utils import ElementHasCssSelector
from class_types import WebElements

from selenium.webdriver.support.ui import WebDriverWait

class Scraper(SeleniumBase):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.base_url = url

    def wait_for_elements_by_css_selector(self, css_selector: str) -> WebElements:
        elements = WebDriverWait(self.webdriver, 10).until(
            ElementHasCssSelector(css_selector)
        )
        return elements

    def process(self) -> None:
        self.log('Beginning scraping process.')
        self.webdriver.get(self.base_url)
        elements = self.wait_for_elements_by_css_selector("a[href='/locations']")
        assert len(elements) == 1
        locations_url = elements[0].get_attribute('href')
        print(locations_url)
        self.log('Ending scraping process.')

if __name__ == '__main__':
    url = 'https://www.onemedical.com/'
    Scraper(url).process()