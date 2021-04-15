from src.utils import WebScraper, ImageGenerator


def handle_web_scraping(args: dict):
    start_len = args['start_len']
    end_len = args['end_len']
    page_count = args['page_count']

    web_scraper = WebScraper()
    for word_len in range(start_len, end_len):
        web_scraper.do(word_len, page_count, True)


def handle_img_generation(args: dict):
    train_test_split = args['train_test_split']
    random_skew = args['random_skew']
    random_blur = args['random_blur']
    img_height = args['img_height']
    img_count = args['img_count']

    image_generator = ImageGenerator(train_test_split, random_skew, random_blur, img_height, img_count)
    image_generator.do()
