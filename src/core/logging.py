import logging

from src.enums import LogLevels


def configure_logging(log_level_str: str):
    log_level_str = log_level_str.upper()

    try:
        log_level = LogLevels[log_level_str]
    except KeyError:
        log_level = LogLevels.error

    logging.basicConfig(
        level=log_level.value, format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.getLogger('habbit_tracker').setLevel(logging.CRITICAL)
