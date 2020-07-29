from class_types import Dict, List, VectorString
from selenium_base import SeleniumBase


class Scraper(SeleniumBase):
    def __init__(
        self, url: str, file_name: str, columns: List[str], headless: bool = False
    ) -> None:
        super().__init__(headless)
        self.base_url = url
        self.file_name = file_name
        self.columns = columns

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.base_url}', '{self.file_name}', {self.columns!r})"

    def __str__(self) -> str:
        return f"Scrapes from {self.base_url} and stores to {self.file_name}"

    def get_office_urls(self) -> VectorString:
        """ Fetches all office urls on One Medical NYC page """
        self.log(f"scrape office urls", type=self.REQ, payload="")
        elements = self.wait_for_elements_by_css_selector("ul.office-list > li p~a")
        self.log(
            f"scrape office urls", type=self.RES, payload=f"{len(elements)} office urls"
        )
        return [a.get_attribute("href") for a in elements]

    def get_office_information(self, url: str) -> Dict:
        """ Fetches office location data on One Medical office page """
        self.log(f"scrape office data", type=self.REQ, payload=url)
        record = dict()
        self.go_to(url)
        selectors = [
            'p[itemprop="streetAddress"]',
            'span[itemprop="addressLocality"]',
            'span[itemprop="addressRegion"]',
            'span[itemprop="postalCode"]',
            'p[itemprop="telephone"]',
        ]
        column_selector_map = dict(zip(self.columns, selectors))
        for key, css_selector in column_selector_map.items():
            if key == "address":
                value = ", ".join(
                    [
                        item.get_attribute("textContent")
                        for item in self.wait_for_elements_by_css_selector(css_selector)
                    ]
                )
            else:
                elements = self.wait_for_elements_by_css_selector(css_selector)
                assert len(elements) == 1
                value = elements[0].get_attribute("textContent")
            record[key] = value
        self.log(f"scrape office data", type=self.RES, payload=f"{record!r}")
        return record

    def process(self) -> None:
        self.log("scrape", type=self.REQ, payload="")
        self.go_to(self.base_url)
        self.go_to_by_href("a[href='/locations']")
        self.go_to_by_href("a[href='/locations/nyc']")
        urls = self.get_office_urls()
        data = [self.get_office_information(url) for url in urls]
        self.write_to_csv(data, self.columns, self.file_name)
        self.log("scrape", type=self.RES, payload=f"{len(data)} records")


if __name__ == "__main__":
    url = "https://www.onemedical.com/"
    x = Scraper(
        url,
        "one_medical_nyc.csv",
        ["address", "city", "state", "zipcode", "phone"],
        True,
    ).process()
