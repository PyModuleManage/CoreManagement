import os
from ConfigFileManager.ConfigException import ConfigException
import configparser

class configFilesManager(object):
    def __init__(self, path_to_config: str, dict_config_allows: str):
        self.path_to_config = path_to_config
        self.dict_config_allows = dict_config_allows
        self.config = None
        self.config_variables = None
        self.config_parser_dict = dict()

        if not os.path.isfile(self.path_to_config):
            raise ConfigException("Config File {}, does not exist".format(
                self.path_to_config))
        if not isinstance(str, self.dict_config_allows):
            raise TypeError("dict_config_allows must be a dict()")


    def ___read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.path_to_config)

    def is_correct_information(self):
        dont_exist_any_sections = True
        for key_dict, values_dict in self.dict_config_allows:
            for key_config in list(self.config.sections()):
                if key_dict in key_config:
                    for key2_dict, values2_dict in values_dict:
                        options = [opt for opt in self.config[key_config]]

                        # If this section doesn't have any option, I assert
                        assert len(options) == 0, "The Section {} is " \
                                                  "empty".format(key_config)

                        if key2_dict in options and values2_dict['required'] \
                                == True:
                            if values2_dict['type'] == 'int':
                                self.parser_config_dict[key_config][
                                    key2_dict] = self.config[key_config][
                                    key2_dict].getint()

                        else:
                            break

                    dont_exist_any_sections = False
                else:
                    break