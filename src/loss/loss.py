import math

import torch
import torch.nn as nn


def debug(loss, logits, labels, prediction_sizes, target_sizes):
    if math.isnan(loss.item()):
        print("loss:", loss)
        print("logits:", logits)
        print("labels:", labels)
        print("prediction_sizes:", prediction_sizes)
        print("target_sizes:", target_sizes)

        raise Exception("NaN loss obtained. But why?")


class OCRCTCLoss(nn.Module):

    def __init__(self, eps: float):
        super(OCRCTCLoss, self).__init__()
        self.eps = eps
        self.loss = nn.CTCLoss(reduction='mean', zero_infinity=True)

    def forward(self, logits, labels, prediction_sizes, target_sizes):
        loss = self.loss(logits, labels, prediction_sizes, target_sizes)
        loss = self.sanitize(loss)

        debug(loss, logits, labels, prediction_sizes, target_sizes)

        return loss

    def sanitize(self, loss):
        if math.isnan(loss.item()) or abs(loss.item() - math.inf) < self.eps:
            return torch.zeros_like(loss)

        return loss
