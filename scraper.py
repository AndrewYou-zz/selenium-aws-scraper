from class_types import Dict, List, VectorString
from selenium_base import SeleniumBase


class Scraper(SeleniumBase):
    def __init__(self, url: str, file_name: str, columns: List[str]) -> None:
        super().__init__()
        self.base_url = url
        self.file_name = file_name
        self.columns = columns

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

    def process(self) -> None:
        self.log("scrape", type=self.REQ, payload="")
        self.go_to(self.base_url)
        self.go_to_locations_page()
        self.go_to_nyc_page()
        urls = self.get_office_urls()
        data = [self.get_office_information(url) for url in urls]
        self.write_to_csv(data, self.columns, self.file_name)
        self.log("scrape", type=self.RES, payload=f"{len(data)} records")


if __name__ == "__main__":
    url = "https://www.onemedical.com/"
    Scraper(
        url, "one_medical_nyc.csv", ["address", "city", "state", "zipcode", "phone"]
    ).process()
