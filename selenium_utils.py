from class_types import WebDriver, WebElements


class ElementHasCssSelector:
    def __init__(self, css_selector: str) -> None:
        self.css_selector = css_selector

    def __call__(self, driver: WebDriver) -> WebElements:
        if (elements := driver.find_elements_by_css_selector(self.css_selector)):
            return elements
        else:
            return False
