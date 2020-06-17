#!/usr/bin/env python
# DataCenter Project
# mysql_access.py
# Store a file (any type of a binary file) to MySQL DB
# Retrieve a file (any type of a binary file) from MySQL DB

# "Usage: mysql_access.py <Function: put_user_pw | get_pw 
#        | put_doc | get_doc | put_image | get_image > <id | filename> <pw>\n")
# For auth: put_user_pw <username> <pw> or get_pw <username>
# For Doc: put_doc <filename> or get_doc <id_md5>
# For Image: put_image <filename> or put_image <id_md5>

# MySQL Access Codes largely from the site below
# https://pynative.com/python-mysql-blob-insert-retrieve-file-image-as-a-blob-in-mysql/

# Every binary file data is encode into base64 code
# Due to the complicated encoding/decoding problems 
# with data containing unicodes (e.g. docx files)

# MySQL library
import mysql.connector
from mysql.connector import Error

# Base64 Encoding/Decoding
import base64

# MD5 Hahsing
import hashlib

import sys

# Global Variables
db_host = 'localhost'
db_name = 'ocr_db'
db_user = 'root'
db_password = 'csci5253'


# Insert username and password to auth table
def insert_user_pw(connection, username, password):
    print("Inserting username %s and password %s into auth table" % 
            (username, password))
    try:
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO auth
                          (username, password) VALUES (%s, %s)"""

        insert_text_tuple = (username, password)
        result = cursor.execute(sql_insert_blob_query, insert_text_tuple)
        connection.commit()
        print("username:%s and password:%s inserted successfully into auth table: %r" % 
                (username, password, result))
    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# Retrieve password of username from auth table for authentication
def get_user_pw(connection, username):
    print("Reading username %s's password from auth table" % (username))
    try:
        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from auth where username = %s"""

        get_blob_tuple = (username,)
        cursor.execute(sql_fetch_blob_query, get_blob_tuple)
        record = cursor.fetchall()

        if (len(record) > 1):
            print("There are more than one record (%d) for %s, %r" %
                     (len(record), username, record))
        else:
            print("record for %s, %r" % (username, record))
        password = ''
        for row in record:
            print("username = %s, password = %s" % (row[0], row[1]))
            password = password + row[1]
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))
        password = ''
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return password


def read_with_filename(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()
    return binary_data


# Insert input BLOB (file binary data) into MySQL doc DB Table
def insert_doc_file(connection, bin_data):
    print("Inserting data into doc table")
    try:
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO doc
                          (id, content) VALUES (%s, %s)"""

        id = hashlib.md5(bin_data).hexdigest()
        content = base64.b64encode(bin_data)

        # Convert data into tuple format
        insert_blob_tuple = (id, content)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Doc file data (id:%s) inserted successfully into doc table: %r" % 
                (id, result))
    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# Insert input BLOB (file binary data) into MySQL image DB Table
def insert_image_file(connection, bin_data):
    print("Inserting data into image table")
    try:
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT INTO image
                          (id, content) VALUES (%s, %s)"""

        id = hashlib.md5(bin_data).hexdigest()
        content = base64.b64encode(bin_data)

        # Convert data into tuple format
        insert_blob_tuple = (id, content)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("image file data (id:%s) inserted successfully into image table: %r" % 
                (id, result))
    except mysql.connector.Error as error:
        print("Failed inserting data into MySQL table {}".format(error))
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


def save_as_filename(bin_data, filename):
    # Store binary data on file system
    with open(filename, 'wb') as file:
        file.write(bin_data)


def get_doc_file(connection, id):
    print("Reading data from a doc table")
    binary_data = b''
    try:
        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from doc where id = %s"""

        get_blob_tuple = (id,)
        cursor.execute(sql_fetch_blob_query, get_blob_tuple)
        record = cursor.fetchall()
        for row in record:
            print("%s_id = %s", row[0])
            binary_data = base64.b64decode(row[1].encode('ascii'))
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))
        binary_data = None

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return binary_data


def get_image_file(connection, id):
    print("Reading data from a image table")
    binary_data = b''
    try:
        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from image where id = %s"""

        get_blob_tuple = (id,)
        cursor.execute(sql_fetch_blob_query, get_blob_tuple)
        record = cursor.fetchall()
        for row in record:
            print("%s_id = %s", row[0])
            binary_data = base64.b64decode(row[1].encode('ascii'))
    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))
        binary_data = None

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
        return binary_data


# START main
def main():
    global db_host
    global db_name
    global db_user
    global db_password

    username = ''
    password = ''

    # Get Arguments
    if len(sys.argv) < 3:
        print ("Usage: mysql_access.py <Function: put_user_pw | get_pw \
            | put_doc | get_doc | put_image | get_image > <id | filename> <pw>\n")
        sys.exit(1)
    print (sys.argv)
    command = sys.argv[1]

    try:
        connection = mysql.connector.connect(host=db_host,
                                             database=db_name,
                                             user=db_user,
                                             password=db_password)
    except mysql.connector.Error as error:
        print("Error Connecting to MySQL DB {}".format(error))

    # Parse command line
    # Insert username and password to auth table
    if command == 'put_user_pw':
        username = sys.argv[2]
        password = sys.argv[3]
        insert_user_pw(connection, username, password)

    # Retrieve password of username from auth table for authentication
    elif command == 'get_pw':
        username = sys.argv[2]
        password = get_user_pw(connection, username)
        print ("username: %s: password: %s" % (username, password))

    # Insert a doc file's content to doc table
    elif command == 'put_doc':
        doc_name = sys.argv[2]
        # If input is not a filename but a binary_data,
        # Remove (Comment out) bin_data = read_with_filename(filename)
        bin_data = read_with_filename(doc_name)
        insert_doc_file(connection, bin_data)

    # Retrieve a doc file's content from doc table with doc_id
    # doc_id is md5 hash of a doc file's content
    elif command == 'get_doc':
        doc_id = sys.argv[2]
        bin_data = get_doc_file(connection, doc_id)
        filename = 'doc_'+doc_id
        # If output is not a filename but a binary_data,
        # Remove (Comment out) bin_data = save_as_filename(bin_data, filename)
        save_as_filename(bin_data, filename)

    # Insert an image file's content to image table
    elif command == 'put_image':
        image_name = sys.argv[2]
        # If input is not a filename but a binary_data,
        # Remove (Comment out) bin_data = read_with_filename(filename)
        bin_data = read_with_filename(image_name)
        insert_image_file(connection, bin_data)

    # Retrieve an image file's content from image table with image_id
    # image_id is md5 hash of an image file's content
    elif command == 'get_image':
        image_id = sys.argv[2]
        bin_data = get_image_file(connection, image_id)
        filename = 'image_'+image_id
        # If output is not a filename but a binary_data,
        # Remove (Comment out) bin_data = save_as_filename(bin_data, filename)
        save_as_filename(bin_data, filename)
    else:
        print ("Usage: mysql_access.py <command: put_user_pw | get_pw \
            | put_doc | get_doc | put_image | get_image | help> <id | filename> <pw>\n")
        sys.exit(1)

    # Create Table: Used for testing purpuses
    # createTable(hostname, dbname, username, pw)
    # createTable(db_host, db_name, db_user, db_password)
# END main


if __name__ == '__main__':
    main()