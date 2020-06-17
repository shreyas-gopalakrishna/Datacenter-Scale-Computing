# https://www.w3schools.com/python/python_mysql_create_db.asp

import mysql.connector
# db_name = 'ocr_db'
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="csci5253"
)
cursor = connection.cursor()

# create_database_query = """CREATE DATABASE `%s` """
create_database_query = """CREATE DATABASE ocr_db """
# create_db_tuple = (db_name,)

cursor.execute(create_database_query)
print("Database ocr_db created successfully")

# cursor.execute("DROP DATABASE `'ocr_db'`")