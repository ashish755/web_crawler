import logging

def configure_logger(logger_name):
    # Create a logger with a specific name
    logger = logging.getLogger(logger_name)

    # Create a formatter with a custom format
    formatter = logging.Formatter("%(asctime)s - %(filename)s - [Line %(lineno)d] - %(levelname)s - %(message)s")

    # Create a file handler that writes log messages to a file
    file_handler = logging.FileHandler('log_file.log')
    file_handler.setLevel(logging.DEBUG) 
    file_handler.setFormatter(formatter) 

    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

    return logger