import mysql.connector

# https://www.w3schools.com/python/python_mysql_create_db.asp
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="csci5253"
)

mycursor = mydb.cursor()

# mycursor.execute("DROP DATABASE `'ocr_db'`")
mycursor.execute("DROP DATABASE ocr_db")