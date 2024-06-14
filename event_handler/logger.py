import logging 

def setup_logger():
    logger =logging.getLogger()
    logger.setLevel(logging.INFO)
    formarter= logging.Formatter(
        '{"level": "%(levelname)s", "date": "%(asctime)s", "message": "%(message)s"}',
        datefmt="%Y-%m-%d %H:%M:%S"
    ) 
    
    consoler_handler= logging.StreamHandler()
    consoler_handler.setFormatter(formarter)
    logger.addHandler(consoler_handler)
    logger.info("Logger started!")
    return logger

LOGGER = setup_logger()