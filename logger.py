import logging

def create_logger(logger_name, log_file):
    logger = logging.getLogger(name=logger_name)
    console = logging.StreamHandler()
    file_logger = logging.FileHandler(filename=log_file)

    LOG_FORMAT = "[%(asctime)s] - [%(agent)s] - [%(levelname)s] - %(message)s"
    file_logger_format = logging.Formatter(LOG_FORMAT)
    file_logger.setFormatter(file_logger_format)
    console.setFormatter(file_logger_format)

    logger.addHandler(file_logger)
    logger.addHandler(console)
    logger.setLevel(logging.DEBUG)

    return logger
