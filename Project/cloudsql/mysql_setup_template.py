#!/usr/bin/env python
# DataCenter Project
# mysql_setup.py
# MySQL DB Setup for auth, put/get doc/image files
# Create DB and Tables

# MySQL Access Codes largely from the site below
# https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/

# Every binary file data is encode into base64 code
# Due to the complicated encoding/decoding problems 
# with data containing unicodes (e.g. docx files)

# MySQL library
import mysql.connector
from mysql.connector import Error

import sys

# Global Variables
db_host = 'localhost'
db_name = 'ocr_db'
# db_name = 'Electronics'
db_user = 'root'
db_password = 'csci5253'
# connection


# Create a talbe for auth (username, password) or similar forms
def create_two_text_table(connection, table_name, id, value):
    try:
        mySql_Create_Table_Query = """CREATE TABLE `%s` ( `%s` TEXT NOT NULL , 
                                `%s` TEXT NOT NULL , PRIMARY KEY (`%s`)) """
        create_table_tuple = (table_name, id, value)

        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query, create_table_tuple)

        print("%s Table with %s, %s created successfully: %r" % 
                (table_name, id, value, result))
    except mysql.connector.Error as error:
        print("Failed to create_two_text_table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")
            # connection.close()
            # print("MySQL connection is closed")


# Create a talbe for doc or image (id_text, doc/image_binary) or similar forms
def create_id_longblob_table(connection, table_name, id, value):
    try:
        mySql_Create_Table_Query = """CREATE TABLE `%s` ( `%s` TEXT NOT NULL , 
                                `%s` LONGBLOB NOT NULL , PRIMARY KEY (`%s`)) """
        create_table_tuple = (table_name, id, value)

        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query, create_table_tuple)

        print("%s Table with %s, %s created successfully: %r" % 
                (table_name, id, value, result))
    except mysql.connector.Error as error:
        print("Failed to create_id_longblob_table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")
            # connection.close()
            # print("MySQL connection is closed")


# Delete all rows in a talbe with the given table name
def delete_all_rows(connection, table_name):
    try:
        Delete_all_rows = """truncate table Laptop """

        cursor = connection.cursor()
        cursor.execute(Delete_all_rows)
        connection.commit()

        print("All Records Deleted successfully in %s table" % (table_name))
    except mysql.connector.Error as error:
        print("Failed to delete all rows in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")
            # connection.close()
            # print("MySQL connection is closed")


# Delete a table with the given table name
def delete_table(connection, table_name):
    try:
        mySql_Delete_Table_Query = """DROP TABLE IF EXISTS `%s` """
        delete_table_tuple = (table_name,)

        cursor = connection.cursor()
        cursor.execute(mySql_Delete_Table_Query, delete_table_tuple)
        connection.commit()
        print("Table %s deleted successfully" % (table_name))
    except mysql.connector.Error as error:
        print("Failed to delete table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")
            # connection.close()
            # print("MySQL connection is closed")


# Delete a database with the given database
def delete_database(connection, db_name):
    try:
        delete_database_query = """DROP DATABASE `%s` """
        delete_db_tuple = (db_name,)

        cursor = connection.cursor()
        cursor.execute(delete_database_query, delete_db_tuple)
        connection.commit()
        print("Database %s deleted successfully" % (db_name))
    except mysql.connector.Error as error:
        print("Failed to delete db in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")
            # connection.close()
            # print("MySQL connection is closed")


# Create a database with the given name
# https://www.w3schools.com/python/python_mysql_create_db.asp
def create_database(db_name):
    global db_host
    # global db_name
    global db_user
    global db_password

    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            passwd=db_password
        )
        cursor = connection.cursor()

        create_database_query = """CREATE DATABASE `%s` """
        create_db_tuple = (db_name,)

        cursor.execute(create_database_query, create_db_tuple)
        print("Database %s created successfully" % (db_name))
    except mysql.connector.Error as error:
        print("Failed to create db in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# START main
def main():
    global db_host
    global db_name
    global db_user
    global db_password
    # global connection

    # Get Arguments
    if len(sys.argv) > 2:
        print ("Usage: mysql_setup.py <create=default | delete>\n")
        sys.exit(1)
    print (sys.argv)
    if len(sys.argv) == 1:
        command = 'create'
    elif len(sys.argv) == 2:
        command = sys.argv[1]

    # Parse command line
    # Create a  talbe for auth (username, password)
    if command == 'create':
        create_database(db_name)

        # Connect to DB
        try:
            connection = mysql.connector.connect(host=db_host,
                                                database=db_name,
                                                user=db_user,
                                                password=db_password)
            create_two_text_table(connection, 'auth', 'username', 'password')
            create_id_longblob_table(connection, 'doc', 'id', 'content')
            create_id_longblob_table(connection, 'image', 'id', 'content')
        except mysql.connector.Error as error:
            print("Error Connecting to MySQL DB {}".format(error))
        finally:
            if (connection.is_connected()):
                connection.close()
                print("MySQL connection is closed")
    elif command == 'delete':
        # Connect to DB
        try:
            connection = mysql.connector.connect(host=db_host,
                                                database=db_name,
                                                user=db_user,
                                                password=db_password)
            # delete_table(connection, 'auth')
            # delete_table(connection, 'doc')
            # delete_table(connection, 'image')

            # Delete all rows in a talbe with the given table name
            # https://pynative.com/python-mysql-delete-data/
            # delete_all_rows(connection, table_name)
            delete_all_rows(connection, 'auth')
            delete_all_rows(connection, 'doc')
            delete_all_rows(connection, 'image')

            # Delete a table with the given table name
            # delete_table(connection, table_name)

            # Delete a database with the given database
            # delete_database(connection, db_name)
            # delete_database(connection, 'Electronics')
        except mysql.connector.Error as error:
            print("Error Connecting to MySQL DB {}".format(error))
        finally:
            if (connection.is_connected()):
                connection.close()
                print("MySQL connection is closed")
    else:
        print ("Usage: mysql_setup.py <create=default | delete>\n")
        sys.exit(1)
# END main


if __name__ == '__main__':
    main()