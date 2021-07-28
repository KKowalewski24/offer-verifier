import logging

from module.constants import LOGS_FILENAME


class Logger:

    def __init__(self) -> None:
        logging.basicConfig(
            filename=LOGS_FILENAME,
            format="[%(asctime)s] {%(pathname)s:%(lineno)d} - %(message)s"
        )


    def debug(self, text: str) -> None:
        logging.debug(text)


    def info(self, text: str) -> None:
        logging.info(text)


    def warning(self, text: str) -> None:
        logging.warning(text)


    def error(self, text: str) -> None:
        logging.error(text)


    def critical(self, text: str) -> None:
        logging.critical(text)
