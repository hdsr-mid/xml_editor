from editors.mwm_xmls import MWM

import logging


def setup_logging():
    """Adds a configured stream handler to the root logger."""
    LOG_LEVEL = logging.INFO
    LOG_DATE_FORMAT = "%H:%M:%S"
    LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

    _logger = logging.getLogger()
    _logger.setLevel(LOG_LEVEL)
    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOG_LEVEL)
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)
    return _logger


if __name__ == "__main__":
    logger = setup_logging()
    MWM.run_mwm()
    logger.info("shutting down")
