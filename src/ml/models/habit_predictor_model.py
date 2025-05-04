import torch.nn as nn
import torch.optim as optim


class HabitPredictor(nn.Module):
    def __init__(self):
        super().__init__()

        self.fc1 = nn.Linear(4, 32)
        self.drop1 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(32, 16)
        self.drop2 = nn.Dropout(0.2)
        self.fc3 = nn.Linear(16, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.drop1(nn.ReLU()(self.fc1(x)))
        x = self.drop2(nn.ReLU()(self.fc2(x)))
        return self.sigmoid(self.fc3(x))


model = HabitPredictor()

optimizer = optim.AdamW(model.parameters(), lr=0.0005, weight_decay=0.001)
loss_func = nn.BCELoss()
