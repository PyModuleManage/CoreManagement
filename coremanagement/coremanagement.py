# coding: utf-8
# Created on: 2018-07-30
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Core Management

:author: Emmanuel Arias
"""

import os

import configparser

from src.ModuleManagement import ModuleManagement as modman

CWD = os.getcwd()
CONFIGURATION_FILE = 'config/config.ini'


class CoreManagement(object):
    def __init__(self):
        self.ip = None
        self.port = None
        self.db_name = None
        self.installation_path = None
        self.mm = None
        self.read_configuration(CONFIGURATION_FILE)
        self.___create_instance_module_management()

    def ___create_instance_module_management(self):
        self.mm = modman(self.ip, self.port, self.db_name,
                         self.installation_path)

    def read_configuration(self, path_to_configuration):
        config = configparser.ConfigParser()
        config.read(path_to_configuration)
        self.ip = config['CONFIG']['IP'].strip()
        self.port = config['CONFIG']['port'].strip()
        self.db_name = config['CONFIG']['DB_NAME'].strip()
        self.installation_path = config['CONFIG']['INSTALL_PATH'].strip()

        if len(self.ip) == 0 and len(self.port) == 0 and \
                len(self.db_name) == 0 and len(self.installation_path) == 0:
            raise Exception('There are not sufficient data on CONFIG_CORE.ini')

    def install(self, module_name, module):
        if os.path.exists(module):
            self.mm.install_module(module_name, module)
        else:
            raise Exception('Does not exist the module package to install')
