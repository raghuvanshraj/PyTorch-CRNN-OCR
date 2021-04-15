import argparse
import sys

import consts
from handlers.handlers import handle_img_generation

INVALID_TRAIN_TEST_SPLIT_SPEC = 'train test split should be between 0 and 1'
INVALID_HEIGHT_SPEC = 'image height should be a strictly positive value'
INVALID_COUNT_SPEC = 'image count should be a non-negative value'

parser = argparse.ArgumentParser(
    description=f'generate images using {consts.WORDS_FILE_PATH}, if file is not available, generate it first'
)
parser.add_argument(
    '--train_test_split',
    type=float,
    help=f'train test split between 0 and 1, defaults to {consts.DEFAULT_TRAIN_TEST_SPLIT}'
)
parser.add_argument(
    '--random_skew',
    action='store_true',
    help=f'determines if images will be randomly skewed'
)
parser.add_argument(
    '--random_blur',
    action='store_true',
    help=f'determines if images will be randomly blurred'
)
parser.add_argument(
    '--height',
    type=int,
    help=f'height of all images, defaults to {consts.DEFAULT_IMG_HEIGHT}'
)
parser.add_argument(
    '--count',
    type=int,
    help=f'total number of images to be generated, if not specified total number of images will be equal to total '
         f'number of words in {consts.WORDS_FILE_PATH} '
)

parser_args = parser.parse_args()
train_test_split = parser_args.train_test_split
random_skew = parser_args.random_skew
random_blur = parser_args.random_blur
img_height = parser_args.height
img_count = parser_args.count

if train_test_split > 1 or train_test_split < 0:
    print(INVALID_TRAIN_TEST_SPLIT_SPEC)
    sys.exit(1)

if img_height <= 0:
    print(INVALID_HEIGHT_SPEC)
    sys.exit(1)

if img_count is not None and img_count < 0:
    print(INVALID_COUNT_SPEC)
    sys.exit(1)

if train_test_split is None:
    train_test_split = consts.DEFAULT_TRAIN_TEST_SPLIT

if img_height is None:
    img_height = consts.DEFAULT_IMG_HEIGHT

x = str
flag = False
while not flag:
    x = input(
        f'''train test split: {train_test_split}
random skew: {random_skew}
random blue: {random_blur}
image height: {img_height}
image count: {img_count}
continue? [y|n] '''
    )
    if x == 'n':
        print('aborting')
        sys.exit(0)

    if x == 'y':
        flag = True
    else:
        print('invalid input, try again')

args = {
    'train_test_split': train_test_split,
    'random_blur': random_blur,
    'random_skew': random_skew,
    'img_height': img_height,
    'img_count': img_count
}
handle_img_generation(args)
