import psutil

from scraper import Scraper


def test_chromedriver_private_path():
    obj = Scraper("https://www.foo.com/", "bar.csv", ["foo1", "foo2", "foo3"], True)
    try:
        print(obj.__path)
    except AttributeError as e:
        if e == "'Scraper' object has no attribute '__path'":
            pass
