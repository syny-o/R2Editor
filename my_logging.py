from datetime import datetime
import logging

# class CustomFormatter(logging.Formatter):

#     green = "\x1b[32;1m"
#     blue = "\x1b[34;1m"
#     grey = "\x1b[38;20m"
#     yellow = "\x1b[33;20m"
#     red = "\x1b[31;20m"
#     bold_red = "\x1b[31;1m"
#     reset = "\x1b[0m"
#     format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

#     FORMATS = {
#         logging.DEBUG: green + format + reset,
#         logging.INFO: blue + format + reset,
#         logging.WARNING: yellow + format + reset,
#         logging.ERROR: red + format + reset,
#         logging.CRITICAL: bold_red + format + reset
#     }

#     def format(self, record):
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)



# # create logger with 'spam_application'
# logger = logging.getLogger("R2 Editor")
# logger.setLevel(logging.DEBUG)

# # create console handler with a higher log level
# my_logger = logging.StreamHandler()
# my_logger.setLevel(logging.DEBUG)

# my_logger.setFormatter(CustomFormatter())

# logger.addHandler(my_logger)


# logger.debug("debug message")
# logger.info("info message")
# logger.warning("warning message")
# logger.error("error message")
# logger.critical("critical message")

# logging.basicConfig(
#     # filename=f"log.log",
#     # format=f"{__name__}--%(asctime)s %(levelname)s %(name)s - %(message)s",
#     level=logging.INFO,
#     # level=logging.CRITICAL,
#     # filemode="w"
# )


# DATE_PREFIX = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# my_logger = logging.getLogger(__name__)
# # my_logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler("file_handler_log.log")
# formatter = logging.Formatter(f"{__name__}--%(asctime)s %(levelname)s %(name)s - %(message)s")
# file_handler.setFormatter(formatter)
# file_handler.setLevel(logging.DEBUG)
# my_logger.addHandler(file_handler)




# # logger_console = logging.getLogger("console_logger")
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# # logger_console.addHandler(console_handler)
# # logger_console.setLevel(logging.INFO)

# my_logger.addHandler(console_handler)



# # logging.basicConfig(
# #     filename=f"log.log",
# #     format=f"{__name__}--%(asctime)s %(levelname)s %(name)s - %(message)s",
# #     level=logging.INFO,
# #     # level=logging.CRITICAL,
# #     # filemode="w"
# # )





# # logging.info("Test")
# my_logger.info("my_Logger_info")
# my_logger.debug("my_Logger_debug")
# # logger_console.critical("consoleLogger")


logger = logging.getLogger("PRDEL")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('file_handler_log.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)



logger.debug("DEBUG TO CONSOLE")

logger.info("ERROR TO FILE")
