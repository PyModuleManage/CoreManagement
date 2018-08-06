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


class DatabaseException(CoreException):
    def __init__(self, *args, **kwargs):
        CoreException.__init__(self, *args, **kwargs)
