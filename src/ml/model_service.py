import logging
from pathlib import Path
import torch

from src.ml.models.habit_predictor_model import HabitPredictor


logger = logging.getLogger('ml.model_service')

class HabitPredictorService:
    def __init__(self):
        self.model = HabitPredictor()
        self.path_to_model = (
            Path(__file__).resolve(strict=True).parent
            / 'models'
            / 'trained'
            / 'predict_model_weights.pth'
        )
        self._device = self._get_device()

    def _get_device(self) -> torch.device:
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def load_model(self):
        state_dict = torch.load(
            self.path_to_model, map_location=self._device, weights_only=True
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
                device=self._device
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