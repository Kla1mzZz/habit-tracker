from pathlib import Path
import torch

from models.predict_model import HabitPredictor


path_to_model = (
    Path(__file__).resolve(strict=True).parent
    / 'models'
    / 'trained'
    / 'predict_model_weights.pth'
)


def predict_model(
    days_this_week: int, habit_today: int, streak_days: int, notes_this_week: int
):
    test_x = torch.tensor(
        [[days_this_week, habit_today, streak_days, notes_this_week]],
        dtype=torch.float32,
    )

    model = HabitPredictor()
    model.load_state_dict(torch.load(str(path_to_model), weights_only=True))
    model.eval()

    with torch.no_grad():
        predict = model(test_x[0])

        return predict.item()
