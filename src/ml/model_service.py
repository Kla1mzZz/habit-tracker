from loguru import logger
import torch

from src.core.config import settings
from src.ml.models.habit_predictor_model import HabitPredictor


class HabitPredictorService:
    def __init__(self):
        self.model = HabitPredictor()
        self._device = self._get_device()

    def _get_device(self) -> torch.device:
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_model(self):
        state_dict = torch.load(
            settings.ml.path_to_model_weights,
            map_location=self._device,
            weights_only=True,
        )

        self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(
        self,
        days_this_week: int,
        habit_today: int,
        streak_days: int,
        notes_this_week: int,
    ) -> float:
        try:
            input_tensor = torch.tensor(
                [[days_this_week, habit_today, streak_days, notes_this_week]],
                dtype=torch.float32,
                device=self._device,
            )

            with torch.no_grad():
                prediction = self.model(input_tensor)
                return prediction.item()

        except Exception as e:
            logger.error(f'Prediction failed: {str(e)}')
            raise


model_service = HabitPredictorService()


def get_model_service() -> HabitPredictorService:
    return model_service
