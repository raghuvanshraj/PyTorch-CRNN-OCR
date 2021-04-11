import torch
import torch.nn as nn
from torch.utils.data.dataset import T_co


class BidirectionalLSTM(nn.Module):

    def __init__(self, n_in: int, n_hidden: int, n_out: int):
        super(BidirectionalLSTM, self).__init__()

        self.rnn = nn.LSTM(input_size=n_in, hidden_size=n_hidden, bidirectional=True)
        self.embedding = nn.Sequential(
            nn.Linear(n_hidden * 2, n_out),
            nn.Softmax(dim=1)
        )

    def forward(self, x) -> T_co:
        self.rnn.flatten_parameters()
        x, _ = self.rnn(x)
        t, b, h = x.size()
        x = x.view(t * b, h)
        x = self.embedding(x)
        x = x.view(t, b, -1)

        return x


class CRNN(nn.Module):

    def __init__(self, cfg: dict):
        super(CRNN, self).__init__()

        self.conv = nn.Sequential()

        conv_out_channels = [64, 128, 256, 256, 512, 512, 512]
        conv_in_channels = [1, 64, 128, 256, 256, 512, 512]
        conv_padding_size = [1, 1, 1, 1, 1, 1, 0]
        conv_stride_size = [1, 1, 1, 1, 1, 1, 1]
        conv_kernel_size = [3, 3, 3, 3, 3, 3, 2]

        def add_conv_module(idx: int, add_max_pool: bool, add_batch_norm: bool):
            self.conv.add_module(f'conv:{idx}', nn.Conv2d(
                conv_in_channels[idx],
                conv_out_channels[idx],
                (conv_kernel_size[idx], conv_kernel_size[idx]),
                (conv_stride_size[idx], conv_stride_size[idx]),
                (conv_padding_size[idx], conv_padding_size[idx])
            ))

            if add_batch_norm:
                self.conv.add_module(f'batch_norm:{idx}', nn.BatchNorm2d(conv_out_channels[idx]))

            self.conv.add_module(f'activation{idx}', nn.ReLU(True))

            if add_max_pool:
                add_max_pool_module(idx)

        max_pool_stride_size = [(2, 2), (2, 2), None, (2, 2), None, (2, 1), None]
        max_pool_kernel_size = [(2, 2), (2, 2), None, (2, 2), None, (2, 1), None]

        def add_max_pool_module(idx: int):
            self.conv.add_module(f'max_pool:{idx}', nn.MaxPool2d(
                kernel_size=max_pool_kernel_size[idx],
                stride=max_pool_stride_size[idx]
            ))

        add_max_pool = [True, True, False, True, False, True, False]
        add_batch_norm = [False, False, False, False, True, True, False]

        for i in range(7):
            add_conv_module(i, add_max_pool[i], add_batch_norm[i])

        assert (cfg['n_in'] is not None) and (cfg['n_hidden'] is not None) and (cfg['n_out'] is not None)
        assert cfg['n_in'] == conv_out_channels[-1]

        self.rnn = nn.Sequential(
            BidirectionalLSTM(cfg['n_in'], cfg['n_hidden'], cfg['n_hidden']),
            BidirectionalLSTM(cfg['n_hidden'], cfg['n_hidden'], cfg['n_out'])
        )

    def forward(self, x: torch.Tensor) -> T_co:
        x = self.conv(x)
        b, c, h, w = x.size()

        assert h == 1

        x = x.squeeze(2)  # (b, c, w)
        x = x.permute(2, 0, 1)  # (w, b, c)
        x = self.rnn(x)  # (t, b, h)
        x = x.transpose(1, 0)  # (b, t, h)

        return x
