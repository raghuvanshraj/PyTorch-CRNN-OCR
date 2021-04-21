import os
from PIL import Image
from glob import glob

import torch.utils.data as data
from torch.utils.data.dataset import T_co
import torchvision.transforms as transforms
import consts


class OCRDataset(data.Dataset):

    def __init__(self, root: os.path, is_train: bool):
        super(OCRDataset, self).__init__()

        self.root = root
        self.subdir = 'train' if is_train else 'test'
        self.data_dir = os.path.join(self.root, self.subdir)
        self.file_format = consts.IMG_FILE_FORMAT
        self.images = os.listdir(self.subdir)
        transform_list = [transforms.Grayscale(1),
                          transforms.ToTensor(),
                          transforms.Normalize((0.5,), (0.5,))]

        self.transform = transforms.Compose(transform_list)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, index) -> T_co:
        assert max(index) <= len(self), 'index range error'
        f = lambda x: os.path.join(self.data_dir, x)
        img_paths = list(map(f, self.images[index]))

        images = []

        for img in img_paths:
            label = os.path.basename(img)
            image = self.transform(Image.open(img))
            images.append({'image': image, 'label': label})

        return images