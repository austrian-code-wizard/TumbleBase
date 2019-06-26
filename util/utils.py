from configparser import ExtendedInterpolation, ConfigParser
from config import config_path
import os


def get_config_parser(file_name):
    """
    Open and parse the config file with the given filename in the config_path directory.
    :param file_name: The name of the configuration file.
    :return: The configuration parser object.
    """
    config_parser = ConfigParser(interpolation=ExtendedInterpolation())
    config_parser.read(os.path.join(config_path, file_name))
    return config_parser


# Define constants for messages that will be presented to the user.
message_config_parser = get_config_parser("messages.ini")
internal_server_error_message = message_config_parser["errors"]["server_error"]
invalid_format_message = message_config_parser["errors"]["invalid_format"]
endpoint_not_found_message = message_config_parser["errors"]["no_endpoint"]
method_not_allowed_message = message_config_parser["errors"]["method_not_allowed"]
could_not_verify_message = message_config_parser["errors"]["could_not_verify"]
invalid_token_message = message_config_parser["errors"]["invalid_token"]
no_admin_message = message_config_parser["errors"]["no_admin"]
invalid_token_message = message_config_parser["errors"]["invalid_token"]