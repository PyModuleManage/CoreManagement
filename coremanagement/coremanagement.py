# coding: utf-8
# Created on: 2018-07-30
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Core Management

:author: Emmanuel Arias
"""
import getopt
import os
import sys

import configparser

from src import ModuleManagement as modman
from src import CoreException

CWD = os.getcwd()
CONFIGURATION_FILE = 'config/config.ini'


class CoreManagement(object):
    def __init__(self):
        self.timeout_database = None
        self.ip = None
        self.port = None
        self.db_name = None
        self.installation_path = None
        self.mm = None
        self.read_configuration(CONFIGURATION_FILE)
        self.___create_instance_module_management()
        if self.___test_connection_to_database() is False:
            raise Exception("DB connection Error")

    def ___test_connection_to_database(self) -> bool:
        if self.mm.test_connection():
            return True
        else:
            return False

    def ___create_instance_module_management(self):
        self.mm = modman.ModuleManagement(self.ip, self.port, self.db_name,
                                          self.installation_path,
                                          self.timeout_database)

    def read_configuration(self, path_to_configuration):
        config = configparser.ConfigParser()
        config.read(path_to_configuration)
        self.ip = config['CONFIG']['IP'].strip()
        # self.port = config['CONFIG']['PORT'].strip()
        self.port = config.getint('CONFIG', 'PORT')
        self.db_name = config['CONFIG']['DB_NAME'].strip()
        self.installation_path = config['CONFIG']['INSTALL_PATH'].strip()
        self.timeout_database = config.getint('CONFIG', 'TIMEOUT_DB_MS')
        if len(self.ip) == 0 and len(self.port) == 0 and \
                len(self.db_name) == 0 and len(self.installation_path) == 0:
            raise Exception('There are not sufficient data on CONFIG_CORE.ini')

    def install(self, module_name, module):
        if os.path.exists(module):
            print('CoreManagement: I will try to install {} ...'.format(
                module_name))
            try:
                self.mm.install_module(module_name, module)
            except CoreException.ErrorInsertElementOnDatabase as error:
                raise CoreException.ErrorInstallationModule("'Some problem "
                                                            "on installation "
                                                            "of module on"
                                                            "CoreManagement'")
            else:
                print('Installation of {} module '
                      'successfully'.format(module_name))


# TODO: Complete the help print
def help():
    sys.exit("""Usage: python coremangement.py {OPTIONS}
    
    OPTIONS:
        -i, --install <name>
            Specify the name of the module to install
        -d, --directory <path/to/module>
            Specify the path to the module to install
        -h, --help
            Print this message.
        --test-connection
            Test connection to DB     
    """)


if __name__ == '__main__':
    # Option parser, check for valid options
    module_name = None
    module_pck = None
    directory_module = None

    try:
        core = CoreManagement()
    except CoreException.TimeOutCoreDatabase as error:
        sys.exit("""Error on DB Connection: {}""".format(error))
    try:
        valid_options = getopt.gnu_getopt(sys.argv[1:],
                                          "i:d:h",
                                          ('install', 'directory', 'help',
                                           'test-connection'))
    except getopt.GetoptError as bad_opt:
        sys.exit(
            "\n coremamagement %s \nTry -h or --help for a list of available "
            "options" % bad_opt)

    for opt, arg in valid_options[0]:
        if opt == '-i' or opt == '--install':
            module_name = arg
        if opt == '-d' or opt == '--directory':
            directory_module = arg
        if opt == '-h' or opt == '--help':
            help()

    if module_name is not None or directory_module is not None:
        try:
            core.install(module_name,directory_module)
        except Exception as error:
            print(error)
