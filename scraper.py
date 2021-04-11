import argparse
import sys

from cmd import handle_web_scraping

INVALID_RANGE_SPEC = 'invalid range specification, please specify range in {uint}-{uint} or {uint} format'
INVALID_PAGE_COUNT_SPEC = 'invalid page range specification, please specify range in {uint} format'

parser = argparse.ArgumentParser(
    description='scrape http://www.yougowords.com/ for words of specified length'
)
parser.add_argument(
    'range',
    type=str,
    help='range of word lengths in {uint}-{uint} or {uint} format'
)
parser.add_argument(
    'page_count',
    type=int,
    help='number of pages to parse for words in {uint} format, one page consists of 50 words'
)

parser_args = parser.parse_args()
len_range = parser_args.range
start_len = int()
end_len = int()
try:
    if '-' in len_range:
        start_len, end_len = map(int, len_range.split('-'))
    else:
        start_len = end_len = int(len_range)
except ValueError:
    print(INVALID_RANGE_SPEC)
    sys.exit(1)

if start_len <= 0 or end_len <= 0:
    print(INVALID_RANGE_SPEC)
    sys.exit(1)

page_count = parser_args.page_count
if page_count <= 0:
    print(INVALID_PAGE_COUNT_SPEC)
    sys.exit(1)

x = str
flag = False
while not flag:
    x = input(
        f'''word length range: {start_len} to {end_len}
page count: {page_count}
continue? [y|n] '''
    )
    if x == 'n':
        print('aborting')
        sys.exit(0)

    if x == 'y':
        flag = True
    else:
        print('invalid input, try again')

end_len += 1

args = {
    'start_len': start_len,
    'end_len': end_len,
    'page_count': page_count
}
handle_web_scraping(args)
