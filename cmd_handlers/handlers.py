from src.utils import WebScraper


def handle_web_scraping(args: dict):
    start_len = args['start_len']
    end_len = args['end_len']

    assert start_len > 0 and end_len > 0

    web_scraper = WebScraper()
    for word_len in range(start_len, end_len):
        print(f'scraping for word length {word_len}')
        web_scraper.scrape(word_len)
