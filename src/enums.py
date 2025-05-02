from enum import StrEnum

class HabitStatus(StrEnum):
    in_progress = 'in_progress'
    pending = 'pending'
    completed = 'completed'
    missed = 'missed'