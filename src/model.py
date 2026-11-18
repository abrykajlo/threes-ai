import torch
import torch.nn as nn

class ThreesModel(nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conv = nn.Conv2d(1, 3, 2)
    
    def forward(self, board, next):
        return self.conv(board)