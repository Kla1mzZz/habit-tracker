from enum import StrEnum


class LogLevels(StrEnum):
    INFO = 'INFO'
    warn = 'WARN'
    error = 'ERROR'
    debug = 'DEBUG'


class HabitStatus(StrEnum):
    in_progress = 'in_progress'
    pending = 'pending'
    completed = 'completed'
    missed = 'missed'
