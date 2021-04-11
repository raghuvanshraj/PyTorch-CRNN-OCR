import os
import re

from bs4 import BeautifulSoup
from selenium import webdriver
import consts


class WebScraper(object):

    def __init__(self):
        self.chrome_webdriver_path = os.path.join(consts.WEBDRIVERS_DIR, 'chromedriver.exe')
        self.base_url = 'http://www.yougowords.com/{0}-letters{1}'
        self.word_regex = '^[a-zA-Z]*$'
        self.words_dir = consts.WORDS_DIR

    def do(self, word_len: int, page_count: int, headless: bool):
        assert page_count > 0

        chrome_options = webdriver.ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_webdriver = webdriver.Chrome(self.chrome_webdriver_path, options=chrome_options)

        for i in range(page_count):
            url = self.base_url.format(word_len, '') if i == 0 else self.base_url.format(word_len, f'-{i + 1}')
            chrome_webdriver.get(url)
            content = chrome_webdriver.page_source
            if content:
                words = self.get_words(content)
                self.save_to_disk(words, word_len)

    def get_words(self, content: str) -> list:
        soup = BeautifulSoup(content, features='html.parser')
        table = soup.find('table', attrs={'id': 'sortable-display'})
        tbody = table.find('tbody')
        word_list = list()
        for tr in tbody.find_all('tr'):
            for td in tr.find_all('td'):
                a = td.find('a')
                if a is not None:
                    words = list(filter(lambda x: x != '', re.findall(self.word_regex, a.text)))
                    if words:
                        word_list.append(*words)

        return word_list

    def save_to_disk(self, word_list: list, word_len: int):
        filepath = os.path.join(self.words_dir, f'{word_len}.txt')
        fp = open(filepath, 'a+', encoding='utf-8')
        write_string = '\n'.join(word_list)
        write_string = f'{write_string}\n'
        fp.write(write_string)
