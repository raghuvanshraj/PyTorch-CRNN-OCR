import os

from scipy.stats import bernoulli
from trdg.generators import GeneratorFromStrings

import consts


class ImageGenerator(object):

    def __init__(self, train_test_split, random_skew, random_blur, img_height, img_count):
        self.train_test_split = train_test_split
        self.random_skew = random_skew
        self.random_blur = random_blur
        self.img_height = img_height
        self.img_count = img_count

        self.img_file_format = consts.IMG_FILE_FORMAT
        self.train_data_dir = consts.TRAIN_DATA_DIR
        self.test_data_dir = consts.TEST_DATA_DIR
        self.words_file_path = consts.WORDS_FILE_PATH

    def do(self):
        self.create_data_dirs()

        fp = open(self.words_file_path, 'r', encoding='utf-8')
        words = fp.read().split()
        count = self.img_count if self.img_count is not None else len(words)
        generator = GeneratorFromStrings(
            words,
            count=count,
            size=self.img_height,
            random_skew=self.random_skew,
            random_blur=self.random_blur
        )

        for img, label in generator:
            file_ext = f'{self.img_file_format}'
            train_flag = bernoulli.rvs(self.train_test_split)

            if train_flag:
                img.save(os.path.join(self.train_data_dir, label + file_ext))
            else:
                img.save(os.path.join(self.test_data_dir, label + file_ext))

    def create_data_dirs(self):
        if not os.path.isdir(self.train_data_dir):
            os.mkdir(self.train_data_dir)
        if not os.path.isdir(self.test_data_dir):
            os.mkdir(self.test_data_dir)
