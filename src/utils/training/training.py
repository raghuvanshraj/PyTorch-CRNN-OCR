import torch.nn as nn
import torch.utils.data as data

import consts


class OCRTrainer(object):

    def __init__(self, model: nn.Module, train_data: data.Dataset, test_data: data.Dataset):
        super(OCRTrainer, self).__init__()

        self.model = model
        self.train_data = train_data
        self.test_data = test_data
        self.batch_size = consts.BATCH_SIZE

        self.train_loader = data.DataLoader(
            train_data,
            batch_size=self.batch_size,
            shuffle=True
        )
        self.test_loader = data.DataLoader(
            test_data,
            batch_size=self.batch_size,
            shuffle=True
        )

    def train(self):
        self.model.train()

    def eval(self):
        self.model.eval()
