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
import logging
import configparser

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(
    os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from src import ModuleManagement as modman
from src import CoreException

CWD = os.getcwd()
CONFIGURATION_FILE = 'config/config.ini'

LOG_PATH = os.path.join(SCRIPT_DIR, 'log/')
if not os.path.exists(os.path.join(LOG_PATH)):

    os.makedirs(os.path.join(LOG_PATH))

logger = logging.getLogger('CoreManagemet')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(os.path.join(LOG_PATH,'coremanagement.log'))
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fh.setFormatter(formatter)
logger.addHandler(fh)

class CoreManagement(object):
    def __init__(self, **kargs):
        if kargs['logger']:
            self.logger = kargs['logger']
        else:
            self.logger = None
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
        if self.logger is not None:
            self.logger.debug('Testing Connection ... ')
        if self.mm.test_connection():
            if self.logger is not None:
                self.logger.debug('Testing connection result: OK')
            return True
        else:
            if self.logger is not None:
                self.logger.debug('Testing connection result: Fail. Please '
                                  'check the connection information or check '
                                  'if mongod start successfully')
            return False

    def ___create_instance_module_management(self):
        self.mm = modman.ModuleManagement(self.ip, self.port, self.db_name,
                                          self.installation_path,
                                          self.timeout_database)

    def read_configuration(self, path_to_configuration):
        if self.logger is not None:
            self.logger.debug('Core management will read the configuration '
                              'file')
            self.logger.debug('The configuration path is: %s'
                              % path_to_configuration)
        config = configparser.ConfigParser()
        config.read(path_to_configuration)
        self.ip = config['CONFIG']['IP'].strip()
        # self.port = config['CONFIG']['PORT'].strip()
        self.port = config.getint('CONFIG', 'PORT')
        self.db_name = config['CONFIG']['DB_NAME'].strip()
        self.installation_path = config['CONFIG']['INSTALL_PATH'].strip()
        self.timeout_database = config.getint('CONFIG', 'TIMEOUT_DB_MS')
        if self.logger is not None:
            self.logger.info('The configuration data to connect to DB are:')
            self.logger.info('IP: %s' % self.ip)
            self.logger.info('PORT: %s' % self.port)
            self.logger.info('DB_NAME: %s' % self.db_name)
            self.logger.info('Installation Path: %s' % self.installation_path)
            self.logger.info('Timeout Database %s' % self.timeout_database)


        if len(self.ip) == 0 and len(self.port) == 0 and \
                len(self.db_name) == 0 and len(self.installation_path) == 0:
            raise Exception('There are not sufficient data on CONFIG_CORE.ini')

    def install(self, module_name: str, module: str):
        """ start the installation of the module

        :param module_name: Module name
        :type module_name: str
        :param module: path to tar.gz of the module
        :type module: str
        :return: None
        :raises CoreException.ErrorInsertElementOnDatabase: Error produce
        when there are some problems on the module installation
        """
        if os.path.exists(module):
            print('CoreManagement: I will try to install {} ...'.format(
                module_name))
            if self.logger is not None:
                self.info('Coremanagement: I will try toi install {} ...'.format(
                    module_name
                ))
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
                if self.logger is not None:
                    self.logger.info('Installation of {} module'
                                     'successfully'.format(module_name))
        else:
            print('The {} module does not exist'.format(module))
            if self.logger is not None:
                self.logger.info('The {} module does not exist'.format(
                    module
                ))


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
        core = CoreManagement(logger=logger)
    except CoreException.TimeOutCoreDatabase as error:
        sys.exit("""Error on DB Connection: {}""".format(error))
    try:
        valid_options = getopt.gnu_getopt(sys.argv[1:],
                                          "i:d:h",
                                          ('install=', 'directory=', 'help',
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
            core.install(module_name, directory_module)
        except CoreException.ErrorInstallationModule as error:
            print("Error of the module installation")
