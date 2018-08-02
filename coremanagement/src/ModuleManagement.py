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

from . import ConfigurationManagement as cm
from . import DatabaseManagement as dm
from . import Package


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

    """
    def __init__(self, ip, port, db_name, packages_folder, timeout_database:
    "Timeout Database" = 1):
        self.timeout_database = timeout_database
        self.ip = ip
        self. port = port
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
            self.list_installed_pck = os.listdir(self.packages_folder)
            l_pck = [pck for pck in self.list_installed_pck if
                     os.path.isdir(pck)]
            self.cnt_installed_pck = len(l_pck)
            return self.list_installed_pck
        except OSError as oserror:
            print("Error: {}".format(oserror))

    def ___connect_to_db(self):
        self.dm = dm.DatabaseManagement(self.ip, self.port, self.db_name,
                                        self.timeout_database)
        self.cm = cm.ConfigurationManagement(self.ip, self.port, self.db_name,
                                             self.timeout_database)

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
        result = self.dm.insert_element(self.collection, rst)
        return result

    def run_module(self, module_name):
        conf = self.read_configuration(module_name)
        buff = dumps(conf)
        buff = loads(buff)
        try:
            self.___exec_module(buff[0]['exec'],
                                buff[0]['parameter'])
        except Exception as error:
            print('Error detected: {}'.format(error))

    @staticmethod
    def ___exec_module(script, parameter=None):
        if parameter is None:
            command = '{}'.format(script)
        else:
            command = '{} {}'.format(script, parameter)
        os.system(command)

    def stop_module(self, module_name):
        conf = self.read_configuration(module_name)
        buff = dumps(conf)
        buff = loads(buff)
        try:
            self.___exec_module(buff[0]['stop_module'])
        except Exception as error:
            print('Error detected: {}'.format(error))

    # TODO: Shall remove the package physically
    def remove_module(self, module_name):
        to_delete = {'module_name': module_name}
        result = self.dm.delete_element(self.collection, to_delete)
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
        if self.dm.test.test_connection():
            return True
        else:
            return False
