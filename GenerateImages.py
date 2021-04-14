import os
from trdg.generators import GeneratorFromStrings
from scipy.stats import bernoulli

root = os.getcwd()
train_path = os.path.join(root, 'data', 'train')
test_path = os.path.join(root, 'data', 'test')
img_format = 'jpg'

filepath = os.path.join(root, 'data\words\words.txt')
file = open(filepath)
words = file.read().split()
file.close()

# os.mkdir(train_path)
# os.mkdir(test_path)

generator = GeneratorFromStrings(words,
                                 count=len(words),
                                 size=32,
                                 random_skew=True,
                                 random_blur=True,)

for img, label in generator:
    train_flag = bernoulli.rvs(0.7)

    if train_flag:
        img.save(os.path.join(train_path, label + '.jpg'))
    else:
        img.save(os.path.join(test_path, label + '.jpg'))