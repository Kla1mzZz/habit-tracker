import torch
import torch.utils.data as data
import torch.nn as nn
import torch.optim as optim

from tqdm import tqdm


n_samples = 1000

days_this_week = torch.randint(0, 8, (n_samples, 1))
habit_done_yesterday = torch.randint(0, 2, (n_samples, 1))
streak_days = torch.randint(0, 30, (n_samples, 1))
notes_this_week = torch.randint(0, 8, (n_samples, 1))

for i in range(n_samples):
    notes_this_week[i] = torch.randint(0, int(days_this_week[i].item()) + 1, (1,))

    
test_x = torch.cat([days_this_week, habit_done_yesterday, streak_days, notes_this_week], dim=1).float()

y = (days_this_week / 7) * 0.35 + (streak_days / 30) * 0.4 + (habit_done_yesterday * 0.10) + (notes_this_week / 7) * 0.15

model = nn.Sequential(
    nn.Linear(4, 8),
    nn.ReLU(),
    nn.Linear(8, 1),
    nn.Sigmoid()
)

optimizer = optim.Adam(model.parameters(), lr=0.0005, weight_decay=0.0001)
loss_func = nn.BCELoss()

epochs = 20
model.train()

epochs_tqdm = tqdm(range(epochs))
for e in epochs_tqdm:
    
    for index, x in enumerate(test_x):
        predict = model(x)
        loss = loss_func(predict, y[index])
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        epochs_tqdm.set_description(f'Epoch [{e+1}/{epochs}]')
        epochs_tqdm.refresh()

torch.save(model.state_dict(), 'predict_model.pth')