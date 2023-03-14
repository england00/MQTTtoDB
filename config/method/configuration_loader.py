import yaml
import logging
from error.configuration_file_error import ConfigurationFileError


def yaml_loader(path):
    try:
        with open(path, 'r') as file:
            params = yaml.safe_load(file)
        return params
    except Exception as e:
        logging.error(str(e))
        raise ConfigurationFileError("ERROR: problem occurred while reading configuration") from None
