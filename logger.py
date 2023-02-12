import logging

# create a logger
logger = logging.getLogger("mylogger")
logger.setLevel(logging.DEBUG)

# create a handler to write log messages to a file
file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(logging.DEBUG)

# create a handler to print log messages to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# create a formatter to include the desired information in the log messages
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s")

# apply the formatter to the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# use the logger in your code
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")