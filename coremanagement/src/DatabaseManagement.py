# coding: utf-8
# Created on: 2018-07-19
# Author: Emmanuel Arias
# E-mail: eamanu@eamanu.com
"""
Database Management
:author: Emmanuel Arias
"""
import pymongo
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class DatabaseManagement(object):
    """This class is use to Database Management

    This class have the methods necessary to:

    - Add
    - Update
    - Delete

    *DatabaseManagement* need 3 variables to be created:

    - :param ip: IP Database
    - :param port: Port Database
    - :param db_name: Database Name
    - :param timeout_database: Timeout of database [ms]
    - :type ip: str
    - :type port: int
    - :type db_name: str
    - :type timeout_database: int

    :Example:

    .. code-block:: console

        >>> dm = DatabaseManagement('localhost', 27017, 'test')
        >>> <DatabaseManagement object at 0x7f100f150250>

    """

    def __init__(self, ip: str, port: int,
                 db_name:str,  timeout_database: "Timeout of database" = 1) \
            -> None:

        self.timeout_database = timeout_database
        self.ip = ip
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None
        self.____connect()

    def ____connect(self) -> None:
        """Connect to Database

        """
        self.client = MongoClient(self.ip, self.port,
                                  serverSelectionTimeoutMS=self.timeout_database)
        self.db = self.client[self.db_name]

    def test_connection(self) -> bool:
        """Test if Database engine is available

        :raise DatabaseException:
        """
        try:
            self.client.server_info()
            return True
        except ServerSelectionTimeoutError as error:
            print("Error: {}".format(error))
            return False

    def get_client(self):
        """Get the client name used

        :returns: self.client. Client name
        :rtype: string

        """
        return self.client

    def insert_element(self, collection, element):
        """Method that insert an element to database

        :param collection: Collection name
        :type collection: str
        :param element: Element to add
        :type element: json
        :return: An instance of InsertOneResult
        :rtype: InsertOneResult
        """
        result = self.db[collection].insert_one(element)
        if isinstance(result, pymongo.results.InsertOneResult):
            return True
        else:
            return False

    def insert_many(self, collection, elements):
        result = self.db[collection].insert_many(elements)
        return result

    def update_element(self, collection, filt, update):
        result = self.db[collection].update_one(filt, update)
        return result

    def delete_element(self, collection, filt):
        result = self.db[collection].delet_one(filt)
        return result

    def show_elements(self, collection, filt=None):
        if filt is None:
            result = self.db[collection].find()
        else:
            result = self.db[collection].find(filt)
        return result
