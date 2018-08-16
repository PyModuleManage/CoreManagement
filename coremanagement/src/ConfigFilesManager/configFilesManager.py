import os
from ConfigFileManager.ConfigException import ConfigException
from ConfigFileManager.ConfigException import KeyNotInConfigFile
from ConfigFileManager.ConfigException import NotValidValueConfig
from ConfigFileManager.ConfigException import RequiredNotExiste
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

    def ___update_parser_config_dict(self, key_config, key2_dict,
                                     value2_dict, required=False):
        try:
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
            raise KeyNotInConfigFile("{} Does not exist on Config File "
                                     "this is required".format(keyerror))
        except ValueError as valueerror:
            raise NotValidValueConfig('Not valid Type: {}'.format(valueerror))

    def is_correct_information(self):
        for key_dict, values_dict in self.dict_config_allows:
            for key_config in list(self.config.sections()):
                if key_dict == key_config:
                    for key2_dict, values2_dict in \
                            self.dict_config_allows[key_config]:
                        options = [opt for opt in self.config[key_config]]

                        # If this section doesn't have any option, I assert
                        assert len(options) == 0, "The Section {} is " \
                                                  "empty".format(key_config)

                        if key2_dict in options and values2_dict['required'] \
                                == True:
                            # First check the required values
                            try:
                                self.___update_parser_config_dict(key_config,
                                                                  key2_dict,
                                                                  values2_dict)
                            except KeyNotInConfigFile as keynoterror:
                                raise RequiredNotExiste('Required '\
                                     'value: {}'.format(keynoterror))
                        if key2_dict in options and values2_dict['required']\
                            == False:
                            # Then check the not required values
                            self.___update_parser_config_dict(key_config,
                                                              key2_dict,
                                                              values2_dict)