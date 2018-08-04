# coding: utf-8
# Created on: 2018-07-26
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Package
:author: Emmanuel Arias
"""

import json
import os
import shutil
import tarfile


class Package(object):
    """Package object

    :param module_name: Module Name
    :type module_name: str
    :param module_package: path to the module
    :type module_package: str
    :param dst_package: path where package are installed
    :type dst_package: str

    """
    def __init__(self, module_name, module_package, dst_package):
        self.module_name = module_name
        self.module_package = module_package  # path to the module
        self.dst_package = dst_package
        self.package_information = None

    def ___uncompress_package(self):
        try:
            shutil.copy(self.module_package, self.dst_package)
            tarfile.open(os.path.join(self.dst_package,
                                         os.path.basename(self.module_package)),
                            'r').extractall(self.dst_package)
            # TODO: maybe we need to rm the .tar.gz package
        except IOError as ioerror:
            print('Error in the copy package to dst: {}'.format(ioerror))

    def read_package_data(self):
        with open(os.path.join(self.dst_package, '{}.json'.format(
                self.module_name))) as json_file:
            data = json.load(json_file)
            if data['package']['module_name'] == self.module_name:
                self.package_information = data
                return True
            else:
                raise Exception('Module name including in the package is not '
                                'given name same')

    def install(self):
        try:
            self.___uncompress_package()
            self.read_package_data()
            return self.package_information
        except Exception as error:
            print('Error: {}'.format(error))
            return False


