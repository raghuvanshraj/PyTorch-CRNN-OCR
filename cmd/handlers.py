from src.utils import WebScraper


def handle_web_scraping(args: dict):
    start_len = args['start_len']
    end_len = args['end_len']
    page_count = args['page_count']

    assert start_len > 0 and end_len > 0 and page_count > 0

    web_scraper = WebScraper()
    for word_len in range(start_len, end_len):
        web_scraper.do(word_len, page_count, True)
