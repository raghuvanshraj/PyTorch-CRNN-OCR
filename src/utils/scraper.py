import os

from bs4 import BeautifulSoup
from selenium import webdriver


class WebScraper(object):

    def __init__(self):
        home = os.path.expanduser('~')
        webdriver_path = os.path.join(home, 'webdrivers')
        self.msedge_webdriver_path = os.path.join(webdriver_path, 'msedgedriver.exe')
        self.base_url = 'http://www.yougowords.com/{0}-letters'

    def scrape(self, word_len: int) -> Exception:
        try:
            msedge_webdriver = webdriver.Edge(self.msedge_webdriver_path)
            url = self.base_url.format(word_len)
            content = msedge_webdriver.get(url)
            soup = BeautifulSoup(content)
        except Exception as err:
            return err
