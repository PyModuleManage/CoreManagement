# coding: utf-8
# Created on: 2018-07-24
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Configuration Management

:author: Emmanuel Arias
"""
from src import DatabaseManagement as dm


class ConfigurationManagement(object):
    """This class manage the module configuration

    """

    def __init__(self, ip: str, port: int, db_name: str,
                 timeout_database: "Timeout database" = 1,
                 **kargs):

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

    def ___connect_to_db(self):
        self.dm = dm.DatabaseManagement(self.ip, self.port, self.db_name,
                                        self.timeout_database)

    def new_configuration(self, module_configs: str) -> dict:
        if self.logger is not None:
            self.logger.debug('New Configuration: %s ' % module_configs)
        result = self.dm.insert_element(self.collection, module_configs)
        return result

    def edit_configuration(self, module_name: str, module_configs:str) -> dict:
        filt = {'module_name': module_name}
        update = {'$set': module_configs}
        if self.logger is not None:
            self.logger.debug('filt: %s' % filt)
            self.logger.debug('update: %s' % update)
        result = self.dm.update_element(self.collection,
                                        filt, update)
        return result

    def remove_configuration(self, module_name: str) -> dict:
        filt = {'module_name': module_name}
        result = self.dm.delete_element(self.collection,
                                        filt)
        if self.logger is not None:
            self.logger.debug('remove_configuration: %s' % result)
        return result

    def stop_configuration(self, module_name: str) -> dict:
        update = {'configuration_status': 'Paused'}
        result = self.edit_configuration(module_name, update)
        return result

    def start_configuration(self, module_name: str) -> dict:
        update = {'configuration_status', 'Started'}
        result = self.edit_configuration(module_name, update)
        return result

    def get_configuration(self, module_name: str) -> dict:
        if not isinstance(module_name, str):
            if self.logger is not None:
                self.logger.warning('Raise Exception: Module name shall be a str instance')
            raise Exception("Module name shall be a str instance")
        fil = {'module_name': module_name}
        result = self.dm.show_elements(self.collection, fil)
        return result
