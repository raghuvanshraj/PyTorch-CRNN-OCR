import os

import torch.utils.data as data
import torchvision.transforms as transforms
from PIL import Image

import consts


class OCRDataset(data.Dataset):

    def __init__(self, is_train: bool):
        super(OCRDataset, self).__init__()

        self.data_dir = consts.TRAIN_DATA_DIR if is_train else consts.TEST_DATA_DIR
        self.file_format = consts.IMG_FILE_FORMAT
        self.images = os.listdir(self.data_dir)
        self.images.sort()
        self.transform = transforms.Compose([
            transforms.Grayscale(consts.N_IMG_CHANNELS),
            transforms.ToTensor(),
            transforms.Normalize((consts.IMG_NORM_MEAN,), (consts.IMG_NORM_STD,))
        ])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx: int) -> dict:
        assert idx < len(self.images), 'index range error'

        image_name = self.images[idx]
        image_path = os.path.abspath(os.path.join(self.data_dir, image_name))
        label = os.path.basename(image_name).lower()
        image = self.transform(Image.open(image_path))

        return {
            'image': image,
            'label': label
        }
