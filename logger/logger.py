from logging.handlers import RotatingFileHandler
from tumbleWeb.util.utils import get_config_parser
import logging
import os


class LoggerFactory:

    @staticmethod
    def _get_path_from_config():
        config_parser = get_config_parser("environment.ini")
        path = config_parser["paths"]["logger"]
        return path

    @staticmethod
    def _create_path_if_not_exists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def _get_logging_level():
        config_parser = get_config_parser("environment.ini")
        level = config_parser["environment"]["logger_level"]
        if level == "debug":
            return logging.DEBUG
        elif level == "info":
            return logging.INFO
        elif level != "debug" and level != "info":
            return None

    @staticmethod
    def _create_logger_with_rotating_handler(name, logging_level, path):
        logger = logging.getLogger(name)
        logger.setLevel(logging_level)
        handler = RotatingFileHandler(path + name + ".log", maxBytes=8192, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def create_logger(name, path=None):
        if path is None:
            path = LoggerFactory._get_path_from_config()
            LoggerFactory._create_path_if_not_exists(path)
        logger_level = LoggerFactory._get_logging_level()
        if logger_level:
            return LoggerFactory._create_logger_with_rotating_handler(name, logger_level, path)
        else:
            return LoggerFactory._create_logger_with_rotating_handler(name, logging.INFO, path)
