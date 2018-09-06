__all__ = ['configFilesManager', 'ConfigException',
           'KeyNotInConfigFile', 'NotValidValueConfig', 'RequiredNotExiste']


class ConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class KeyNotInConfigFile(KeyError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class NotValidValueConfig(ValueError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class RequiredNotExiste(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message