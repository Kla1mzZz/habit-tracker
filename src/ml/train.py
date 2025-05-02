from pathlib import Path
import torch
import pandas as pd
from torch.utils.data import TensorDataset, DataLoader
from tqdm import tqdm

from models.habit_predictor_model import model, optimizer, loss_func


path_to_train_data = (
    Path(__file__).resolve(strict=True).parent / 'data' / 'habits_data.csv'
)

df = pd.read_csv(path_to_train_data)

X = df[['day_of_week', 'habit_today', 'streak_days', 'notes']].values
y = df['motivation'].values

X_tensor = torch.tensor(X, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.float32).view(-1, 1)

dataset = TensorDataset(X_tensor, y_tensor)
loader = DataLoader(dataset, batch_size=32, shuffle=True)


epochs = 200
model.train()

epochs_tqdm = tqdm(range(epochs))
for e in epochs_tqdm:
    for x_batch, y_batch in loader:
        predict = model(x_batch).squeeze()
        loss = loss_func(predict, y_batch.squeeze())

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    epochs_tqdm.set_description(f'Epoch [{e + 1}/{epochs}] Loss: {loss.item():.4f}')
    epochs_tqdm.refresh()


path_save_model = (
    Path(__file__).resolve(strict=True).parent
    / 'models'
    / 'trained'
    / 'predict_model_weights.pth'
)

torch.save(model.state_dict(), str(path_save_model))
