# coding: utf-8
# Created on: 2018-08-05
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Core Management

:author: Emmanuel Arias
"""
import pprint


class CoreException(Exception):
    def __init__(self,  *args, **kwargs):
        message = ''
        if args is not None:
            for arg in args:
                if arg == 'TimeOutConnection':
                    message = "An Error has been occurred during the " \
                                   "connection to DataBase Engine"
                if kwargs is not None:
                    for k, v in kwargs.items():
                        if k == 'params_error':
                            Exception.__init__(self, message)
                            print("Exception parameters:")
                            pprint.pprint(v)


class ErrorInstallationModule(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DatabaseException(Exception):
    def __init__(self, message: str, errors: dict = None):
        super().__init__(message)
        self.message = message
        self.errors = errors

        if self.errors is not None:
            pprint.pprint(self.errors)


class TimeOutCoreDatabase(DatabaseException):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ErrorInsertElementOnDatabase(DatabaseException):
    def __init__(self, message: str,
                 collection: str = None, element: str = None):
        self.message = message + " "
        if collection is not None:
            self.message = self.message + "collection: " + collection + " "
            if element is not None:
                self.message = self.message + "element: " + element
        super().__init__(self.message)


class ErrorInsertManyElementOnDatabase(ErrorInsertElementOnDatabase):
    def __init__(self, message: str,
                 collection: str = None,
                 element: str = None):
        super().__init__(message, collection, element)

