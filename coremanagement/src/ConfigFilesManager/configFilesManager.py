import os
# import sys

from ConfigExceptions import ConfigException
from ConfigExceptions import KeyNotInConfigFile
from ConfigExceptions import NotValidValueConfig
from ConfigExceptions import RequiredNotExiste
import configparser


class configFilesManager(object):
    def __init__(self, path_to_config: str, dict_config_allows: dict):
        self.path_to_config = path_to_config
        self.dict_config_allows = dict_config_allows
        self.config = None
        self.config_variables = None
        self.parser_config_dict = dict()

        if not os.path.isfile(self.path_to_config):
            raise ConfigException("Config File {}, does not exist".format(
                self.path_to_config))
        if not isinstance(self.dict_config_allows, dict):
            raise TypeError("dict_config_allows must be a dict()")

        #  Read de config
        self.___read_config()

    def ___read_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.path_to_config)

    def ___update_parser_config_dict(self, key_config, key2_dict,
                                     value2_dict, required=False):
        try:
            if key_config not in self.parser_config_dict.keys():
                self.parser_config_dict[key_config] = dict()
            else:
                pass

            if value2_dict['type'] == 'int':
                self.parser_config_dict[key_config][key2_dict] = \
                    self.config.getint(key_config, key2_dict)
                flag_used = True

            elif value2_dict['type'] == 'float':
                self.parser_config_dict[key_config][key2_dict] = \
                    self.config.getfloat(key_config, key2_dict)
                flag_used = True

            elif value2_dict['type'] == 'bool':
                self.parser_config_dict[key_config][key2_dict] = \
                    self.config.getboolean(key_config, key2_dict)
                flag_used = True

            elif value2_dict['type'] == 'str':
                self.parser_config_dict[key_config][key2_dict] = \
                    self.config[key_config][key2_dict]
                flag_used = True
            else:
                self.parser_config_dict[key_config][key2_dict] = \
                    self.config[key_config][key2_dict]
                flag_used = True

        except KeyError as keyerror:
            if required:
                raise KeyNotInConfigFile("{} Does not exist on Config File "
                                         "this is required".format(keyerror))
            else:
                pass

        except ValueError as valueerror:
            raise NotValidValueConfig('Not valid Type: {}'.format(valueerror))

    def is_correct_information(self):
        for key_dict, values_dict in self.dict_config_allows.items():
            for key_config in list(self.config.sections()):
                if key_dict == key_config:
                    for key2_dict, values2_dict in \
                            self.dict_config_allows[key_config].items():
                        options = [opt for opt in self.config[key_config]]

                        if key2_dict.lower() in options and values2_dict[
                            'required'] \
                                == True:
                            # First check the required values
                            try:
                                self.___update_parser_config_dict(key_config,
                                                                  key2_dict,
                                                                  values2_dict)
                            except KeyNotInConfigFile as keynoterror:
                                raise RequiredNotExiste('Required '\
                                     'value: {}'.format(keynoterror))
                        if key2_dict.lower() in options and values2_dict[
                            'required']\
                            == False:
                            # Then check the not required values
                            self.___update_parser_config_dict(key_config,
                                                              key2_dict,
                                                              values2_dict)