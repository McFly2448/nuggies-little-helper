import logging

def setup_logger(name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
            datefmt='%H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger