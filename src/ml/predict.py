import torch
import torch.nn as nn


model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid()
)

days_this_week = 2
habit_done_yesterday = 0
streak_days = 15
notes_this_week = 0

test_x = torch.tensor([[days_this_week, habit_done_yesterday, streak_days, notes_this_week]], dtype=torch.float32)

model.load_state_dict(torch.load('predict_model.pth', weights_only=True))
model.eval()

with torch.no_grad():
    predict = model(test_x[0])
    
    print(f'{int(predict.item() * 100)}%')