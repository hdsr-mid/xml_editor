from editors.mwm_xmls import MWM

import logging


def setup_logging():
    """Adds a configured stream handler to the root logger."""
    log_level = logging.INFO
    log_date_format = "%H:%M:%S"
    log_format = "%(asctime)s %(levelname)s %(message)s"

    _logger = logging.getLogger()
    _logger.setLevel(log_level)
    formatter = logging.Formatter(fmt=log_format, datefmt=log_date_format)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(formatter)
    _logger.addHandler(stream_handler)
    return _logger


if __name__ == "__main__":
    logger = setup_logging()
    MWM.run_mwm()
    logger.info("shutting down")
