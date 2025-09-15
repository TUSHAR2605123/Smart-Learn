# create databse Connectivity for smartlearn database and users table

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mysql@pranav1",
  database="smartlearn"
)

mycursor = mydb.cursor()
# test connection
mycursor.execute("SELECT DATABASE()")
database_name = mycursor.fetchone()
print("Connected to database:", database_name)
#Get smart learn tables and its columns
mycursor.execute("SHOW TABLES")
tables = mycursor.fetchall()
for table in tables:
    print("Table:", table[0])
    mycursor.execute(f"SHOW COLUMNS FROM {table[0]}")
    columns = mycursor.fetchall()
    for column in columns:
        print(" -", column[0])