#!/usr/bin/env python
# DataCenter Project
# mysql_setup.py
# MySQL DB Setup for auth, put/get doc/image files
# Create DB and Tables
# "Usage: mysql_setup.py <create=default | delete>\n"

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


# Create a talbe for auth (username, password)
def create_auth_table(connection):
    try:
        mySql_Create_Table_Query = """CREATE TABLE auth ( username varchar(32) NOT NULL , 
                                password varchar(256) NOT NULL , PRIMARY KEY (username)) """

        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)
        print("auth Table created successfully: %r" % result)
    except mysql.connector.Error as error:
        print("Failed to create_auth_table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Create a talbe for doc binary
def create_doc_table(connection):
    try:
        mySql_Create_Table_Query = """CREATE TABLE doc ( id varchar(32) NOT NULL , 
                                content LONGBLOB NOT NULL , PRIMARY KEY (id)) """
        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)

        print("doc Table created successfully: %r" % result)
    except mysql.connector.Error as error:
        print("Failed to create_doc_table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Create a talbe for doc binary
def create_image_table(connection):
    try:
        mySql_Create_Table_Query = """CREATE TABLE image ( id varchar(32) NOT NULL , 
                                content LONGBLOB NOT NULL , PRIMARY KEY (id)) """
        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)

        print("image Table created successfully: %r" % result)
    except mysql.connector.Error as error:
        print("Failed to create_image_table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete all rows in auth talbe with the given table name
def delete_auth_all_rows(connection):
    try:
        Delete_all_rows = """truncate table auth """

        cursor = connection.cursor()
        cursor.execute(Delete_all_rows)
        connection.commit()

        print("All Records Deleted successfully in auth table")
    except mysql.connector.Error as error:
        print("Failed to delete all rows in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete all rows in doc talbe with the given table name
def delete_doc_all_rows(connection):
    try:
        Delete_all_rows = """truncate table doc """

        cursor = connection.cursor()
        cursor.execute(Delete_all_rows)
        connection.commit()

        print("All Records Deleted successfully in doc table")
    except mysql.connector.Error as error:
        print("Failed to delete all rows in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete all rows in image talbe with the given table name
def delete_image_all_rows(connection):
    try:
        Delete_all_rows = """truncate table image """

        cursor = connection.cursor()
        cursor.execute(Delete_all_rows)
        connection.commit()

        print("All Records Deleted successfully in image table")
    except mysql.connector.Error as error:
        print("Failed to delete all rows in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete a table with the given table name
def delete_table_auth(connection):
    try:
        mySql_Delete_Table_Query = """DROP TABLE IF EXISTS auth """

        cursor = connection.cursor()
        cursor.execute(mySql_Delete_Table_Query)
        connection.commit()
        print("Table auth deleted successfully")
    except mysql.connector.Error as error:
        print("Failed to delete table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete a table with the given table name
def delete_table_doc(connection):
    try:
        mySql_Delete_Table_Query = """DROP TABLE IF EXISTS doc """

        cursor = connection.cursor()
        cursor.execute(mySql_Delete_Table_Query)
        connection.commit()
        print("Table doc deleted successfully")
    except mysql.connector.Error as error:
        print("Failed to delete table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete a table with the given table name
def delete_table_image(connection):
    try:
        mySql_Delete_Table_Query = """DROP TABLE IF EXISTS image """

        cursor = connection.cursor()
        cursor.execute(mySql_Delete_Table_Query)
        connection.commit()
        print("Table image deleted successfully")
    except mysql.connector.Error as error:
        print("Failed to delete table in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Delete a database with the given database
def delete_ocr_db_database(connection, db_name):
    try:
        delete_database_query = """DROP DATABASE ocr_db """

        cursor = connection.cursor()
        cursor.execute(delete_database_query)
        connection.commit()
        print("Database ocr_db deleted successfully")
    except mysql.connector.Error as error:
        print("Failed to delete db in MySQL: {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            print("MySQL cursor is closed")


# Create a database with the given name: ocr_db
# https://www.w3schools.com/python/python_mysql_create_db.asp
def create_ocr_db_database():
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

        create_database_query = """CREATE DATABASE ocr_db """

        cursor.execute(create_database_query)
        print("Database ocr_db created successfully")
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
        # Create a database: ocr_db fixed
        # create_ocr_db_database()

        # Connect to DB
        try:
            connection = mysql.connector.connect(host=db_host,
                                                database=db_name,
                                                user=db_user,
                                                password=db_password)
            create_auth_table(connection)
            create_doc_table(connection)
            create_image_table(connection)
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
            
            # Delete all rows in a talbe with the given table name
            # https://pynative.com/python-mysql-delete-data/
            # delete_all_rows(connection, table_name)
            delete_auth_all_rows(connection)
            delete_doc_all_rows(connection)
            delete_image_all_rows(connection)

            # Delete a table with the given table name
            # delete_table_auth(connection)
            # delete_table_doc(connection)
            # delete_table_image(connection)

            # Delete a database with the given database
            # delete_ocr_db_database()
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