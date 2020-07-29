import csv

from selenium.webdriver.support.ui import WebDriverWait

from base import SeleniumBase
from class_types import Dict, List, VectorDict, VectorString, WebElements
from selenium_utils import ElementHasCssSelector


class Scraper(SeleniumBase):
    def __init__(self, url: str, file_name: str, columns: List[str]) -> None:
        super().__init__()
        self.base_url = url
        self.file_name = file_name
        self.columns = columns

    def go_to(self, url: str) -> None:
        self.log(f"navigate to", type=self.REQ, payload=url)
        self.webdriver.get(url)
        self.log(f"navigate to", type=self.RES, payload=url)

    def wait_for_elements_by_css_selector(
        self, css_selector: str, wait_time: int = 10
    ) -> WebElements:
        self.log(f"waiting for css selector", type=self.REQ, payload=css_selector)
        elements = WebDriverWait(self.webdriver, wait_time).until(
            ElementHasCssSelector(css_selector)
        )
        self.log(
            f"waiting for css selector",
            type=self.RES,
            payload=f"{len(elements)} elements",
        )
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

    def get_office_urls(self) -> VectorString:
        self.log(f"scrape office urls", type=self.REQ, payload="")
        elements = self.wait_for_elements_by_css_selector("ul.office-list > li p~a")
        self.log(
            f"scrape office urls", type=self.RES, payload=f"{len(elements)} office urls"
        )
        return [a.get_attribute("href") for a in elements]

    def get_office_information(self, url: str) -> Dict:
        self.log(f"scrape office data", type=self.REQ, payload=url)
        self.go_to(url)
        address = ", ".join(
            [
                item.get_attribute("textContent")
                for item in self.wait_for_elements_by_css_selector(
                    'p[itemprop="streetAddress"]'
                )
            ]
        )
        city = self.wait_for_elements_by_css_selector(
            'span[itemprop="addressLocality"]'
        )
        assert len(city) == 1
        city = city[0].get_attribute("textContent")
        state = self.wait_for_elements_by_css_selector('span[itemprop="addressRegion"]')
        assert len(state) == 1
        state = state[0].get_attribute("textContent")
        zipcode = self.wait_for_elements_by_css_selector('span[itemprop="postalCode"]')
        assert len(zipcode) == 1
        zipcode = zipcode[0].get_attribute("textContent")
        phone = self.wait_for_elements_by_css_selector('p[itemprop="telephone"]')
        assert len(phone) == 1
        phone = phone[0].get_attribute("textContent")
        record = {
            "address": address,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "phone": phone,
        }
        self.log(f"scrape office data", type=self.RES, payload=f"{record!r}")
        return record

    def write_to_csv(self, data: VectorDict) -> None:
        self.log("write to csv", type=self.REQ, payload=self.file_name)
        with open(self.file_name, "w") as file:
            csvwriter = csv.DictWriter(file, fieldnames=self.columns)
            csvwriter.writeheader()
            csvwriter.writerows(data)
        self.log("write to csv", type=self.RES, payload=self.file_name)

    def process(self) -> None:
        self.log("scrape", type=self.REQ, payload="")
        self.go_to(self.base_url)
        self.go_to_locations_page()
        self.go_to_nyc_page()
        urls = self.get_office_urls()
        data = [self.get_office_information(url) for url in urls]
        self.write_to_csv(data)
        self.log("scrape", type=self.RES, payload=f"{len(data)} records")


if __name__ == "__main__":
    url = "https://www.onemedical.com/"
    Scraper(
        url, "one_medical_nyc.csv", ["address", "city", "state", "zipcode", "phone"]
    ).process()
