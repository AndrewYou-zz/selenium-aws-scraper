from base import SeleniumBase

class Scraper(SeleniumBase):
    def process(self):
        self.log('Beginning scraping process.')
        self.log('Ending scraping process.')
        pass

if __name__ == '__main__':
    Scraper().process()