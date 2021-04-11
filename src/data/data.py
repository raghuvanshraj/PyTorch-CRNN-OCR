import os
from glob import glob

import torch.utils.data as data
from torch.utils.data.dataset import T_co


class OCRDataset(data.Dataset):

    def __init__(self, root: os.path, is_train: bool, file_ext: str):
        super(OCRDataset, self).__init__()

        self.root = root
        self.subdir = 'train' if is_train else 'test'
        self.data_dir = os.path.join(self.root, self.subdir)
        self.file_ext = file_ext

    def __len__(self):
        pass

    def __getitem__(self, index: int) -> T_co:
        pass
