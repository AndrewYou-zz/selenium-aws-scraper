from class_types import Dict
from scraper import Scraper


def handler(event: Dict, context: Dict) -> None:
    url = "https://www.onemedical.com/"
    x = Scraper(
        url, "one_medical_nyc.csv", ["address", "city", "state", "zipcode", "phone"]
    ).process()


if __name__ == "__main__":
    handler({}, {})
