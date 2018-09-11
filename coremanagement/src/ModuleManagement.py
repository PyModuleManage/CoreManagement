# coding: utf-8
# Created on: 2018-07-19
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Module Management

:author: Emmanuel Arias
"""

import os

from bson.json_util import dumps
from bson.json_util import loads

from src import ConfigurationManagement as cm
from src import DatabaseManagement as dm
from src import Package


class ModuleManagement(object):
    """This Class manage the installation of new module on the core

    This Class use the information necessary to run a
    installed module.

    :param ip: Database IP
    :type ip: str
    :param port: Database port
    :type port: int
    :param db_name: Database Name
    :type db_name: str
    :param packages_folder: Path to packages folder installed
    :type packages_folder: str
    :param kargs: Multiple parameters:

        *logger= Logger objet to write system log

    :type kargs: dict

    """

    def __init__(self, ip: str, port: int, db_name: str,
                 packages_folder: str,
                 timeout_database: int = 1, **kargs: dict):

        if 'logger' in kargs:
            self.logger = kargs['logger']
        else:
            self.logger = None
        self.timeout_database = timeout_database
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.dm = None
        self.collection = 'ModuleConfiguration'
        self.___connect_to_db()
        self.packages_folder = packages_folder
        self.cm = None
        self.cnt_installed_pck = 0
        self.list_installed_pck = list()

    def ___get_packages_installed(self):
        try:
            self.logger.debug('Getting list of installed packages')
            self.list_installed_pck = os.listdir(self.packages_folder)
            l_pck = [pck for pck in self.list_installed_pck if
                     os.path.isdir(pck)]
            self.cnt_installed_pck = len(l_pck)
            self.logger.info('There are {} packages installed'.format(
                self.cnt_installed_pck
            ))
            self.logger.debug('The list of packages installed is: %s ' %
                              self.list_installed_pck)
            return self.list_installed_pck
        except OSError as oserror:
            self.logger.error('Error: oserror')
            print("Error: {}".format(oserror))

    def ___connect_to_db(self):
        if self.logger is not None:
            self.logger.debug('Checking Connection to DB')
        self.dm = dm.DatabaseManagement(self.ip, self.port, self.db_name,
                                        self.timeout_database)
        self.cm = cm.ConfigurationManagement(self.ip, self.port, self.db_name,
                                             self.timeout_database)
        if self.logger is not None:
            self.logger.debug('Checking Connection to DB: OK')

    def read_configuration(self, module_name):
        result = self.cm.get_configuration(module_name)
        return result

    def install_module(self, module_name, module_package):
        """Installation method.

        This method install a package on the `self.packages_folder` and
        insert the module information into the database

        :param module_name: Module name
        :type module_name: str
        :param module_package: Path to the module pacakge
        :type module_package: str
        :return: An instance of InsertOneResult
        :rtype: InsertOneResult
        """
        package = Package.Package(module_name, module_package,
                                  self.packages_folder)
        rst = package.install()
        if rst is False:
            self.logger.error('Error on package installation')
            raise Exception("Error on package installation")
        self.dm.insert_element(self.collection, rst)

    def run_module(self, module_name):
        conf = self.read_configuration(module_name)
        buff = dumps(conf)
        buff = loads(buff)
        try:
            self.___exec_module(buff[0]['exec'],
                                buff[0]['parameter'])
        except Exception as error:
            self.logger.error
            print('Error detected: {}'.format(error))

    @staticmethod
    def ___exec_module(script, parameter=None):
        if parameter is None:
            command = '{}'.format(script)
        else:
            command = '{} {}'.format(script, parameter)
        self.logger.info('I will run: %s' % command)
        os.system(command)

    def stop_module(self, module_name):
        conf = self.read_configuration(module_name)
        buff = dumps(conf)
        buff = loads(buff)
        try:
            self.___exec_module(buff[0]['stop_module'])
        except Exception as error:
            self.logger.error('Error detected: %s' % error)
            print('Error detected: {}'.format(error))

    # TODO: Shall remove the package physically
    def remove_module(self, module_name):
        to_delete = {'module_name': module_name}
        result = self.dm.delete_element(self.collection, to_delete)
        self.logger.info('I will delete the %s' % module_name)
        return result

    # TODO: complete this method
    def get_access(self):
        """This method is used to get the access for user
        to some modules.

        :Parameters:

        TBD

        :Returns:

        TBD
        """
        pass

    def test_connection(self) -> bool:
        self.logger.info('Testing connection ... ')
        if self.dm.test_connection():
            self.logger.info('Connection OK')
            return True
        else:
            self.logger.info('Connection NOK')
            return False
