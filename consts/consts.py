import os

HOME_DIR = os.path.expanduser('~')
DATA_ROOT_DIR = 'data'
WORDS_DATA_DIR = os.path.join(DATA_ROOT_DIR, 'words')
WORDS_FILE_PATH = os.path.join(WORDS_DATA_DIR, 'words.txt')
TRAIN_DATA_DIR = os.path.join(DATA_ROOT_DIR, 'train')
TEST_DATA_DIR = os.path.join(DATA_ROOT_DIR, 'test')
WEBDRIVERS_DIR = os.path.join(HOME_DIR, 'webdrivers')
IMG_FILE_FORMAT = '.jpg'

# default config values
DEFAULT_TRAIN_TEST_SPLIT = 0.7
DEFAULT_IMG_HEIGHT = 32
