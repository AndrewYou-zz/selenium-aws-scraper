import psutil

from scraper import Scraper


def test_chromedriver_private_path():
    x = Scraper("https://www.foo.com/", "bar.csv", ["foo1", "foo2", "foo3"],)
    try:
        print(x.__path)
    except AttributeError as e:
        if e == "'Scraper' object has no attribute '__path'":
            pass
