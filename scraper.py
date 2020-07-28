from selenium.webdriver.support.ui import WebDriverWait

from base import SeleniumBase
from class_types import WebElements
from selenium_utils import ElementHasCssSelector


class Scraper(SeleniumBase):
    def __init__(self, url: str) -> None:
        super().__init__()
        self.base_url = url

    def go_to(self, url: str) -> None:
        self.log(f"Navigating to {url}.")
        self.webdriver.get(url)
        self.log(f"Navigated to {url}.")

    def wait_for_elements_by_css_selector(self, css_selector: str) -> WebElements:
        self.log(f"Waiting for {css_selector!r}.")
        elements = WebDriverWait(self.webdriver, 10).until(
            ElementHasCssSelector(css_selector)
        )
        self.log(f"Found {len(elements)} {css_selector!r} elements.")
        return elements

    def go_to_locations_page(self) -> None:
        elements = self.wait_for_elements_by_css_selector("a[href='/locations']")
        assert len(elements) == 1
        locations_url = elements[0].get_attribute("href")
        self.go_to(locations_url)

    def go_to_nyc_page(self) -> None:
        elements = self.wait_for_elements_by_css_selector("a[href='/locations/nyc']")
        assert len(elements) == 1
        nyc_url = elements[0].get_attribute("href")
        self.go_to(nyc_url)

    def process(self) -> None:
        self.log("Beginning scraping process.")
        self.go_to(self.base_url)
        self.navigate_to_locations_page()
        self.navigate_to_nyc_page()
        self.log("Ending scraping process.")


if __name__ == "__main__":
    url = "https://www.onemedical.com/"
    Scraper(url).process()
