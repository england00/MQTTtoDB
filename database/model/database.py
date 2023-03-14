import logging
import mysql.connector
from mysql.connector import Error
from interfaces.database.interface_database import IDatabase


class MySQLDatabase(IDatabase):

    def __init__(self, host_name, user_name, user_password, charset):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password
        self.charset = charset
        self.connection = None
        self.cursor = None

    # STARTING CONNECTION
    def start_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host_name,
                user=self.user_name,
                passwd=self.user_password,
                charset=self.charset
            )
            print("MySQL connection done successfully (host = '{}', user = '{}')".
                  format(self.host_name, self.user_name))
        except Error as err:
            logging.error(str(err))

    # CLOSING CONNECTION
    def close_connection(self):
        try:
            self.connection.close()
            print("MySQL connection closed successfully (host = '{}', user = '{}')".
                  format(self.host_name, self.user_name))
        except Error as err:
            logging.error(str(err))

    # DATABASE CREATION
    def create_database(self, database_name):
        self.cursor = self.connection.cursor()
        try:
            query = "CREATE DATABASE {}".format(database_name)
            self.cursor.execute(query)
            print("Creation of '{}' done successfully".format(database_name))
        except Error as err:
            logging.error(str(err))

    # CHOOSING DATABASE
    def choose_database(self, database_name):
        self.cursor = self.connection.cursor()
        try:
            query = "USE {}".format(database_name)
            self.cursor.execute(query)
            print("Choice of '{}' done successfully".format(database_name))
        except Error as err:
            logging.error(str(err))

    # DATABASE DESTRUCTION
    def destroy_database(self, database_name):
        self.cursor = self.connection.cursor()
        try:
            query = "DROP DATABASE {}".format(database_name)
            self.cursor.execute(query)
            print("Destruction of '{}' done successfully".format(database_name))
        except Error as err:
            logging.error(str(err))

    # READING QUERY
    def read_query(self, query):
        self.cursor = self.connection.cursor()
        try:
            self.connection.commit()
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as err:
            logging.error(str(err))

    # WRITING QUERIES
    def execute_query(self, query):
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as err:
            logging.error(str(err))
