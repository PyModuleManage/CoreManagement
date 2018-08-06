# coding: utf-8
# Created on: 2018-08-05
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Core Management

:author: Emmanuel Arias
"""


class CoreException(Exception):
    def __init__(self, param_error=None, *args, **kwargs):
        self.param_error = param_error

        if kwargs is not None:
            for k, v in kwargs.items():
                if k == 'message':
                    Exception.__init__(self, v)


class DatabaseException(CoreException):
    def __init__(self, param_error=None, *args, **kwargs):
        CoreException.__init__(self,param_error, *args, **kwargs)


