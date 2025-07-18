#the code with be responsible for connecting to the SQLite database and executing queries
import sqlite3

# Function to connect to the SQLite database
def connect_to_db(db_name):
    try:
        conn = sqlite3.connect(db_name)
        print(f"Connected to the database: {db_name}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Connecting to the database
connection = connect_to_db('example.db')

#creating a cursor object to execute SQL commands
cursor = connection.cursor()

#creating a table
table_info = """

CREATE TABLE STUDENT(NAME VARCHAR(25), AGE INT, ADDRESS VARCHAR(50), MARKS INT);
"""

cursor.execute(table_info) #creating a table with the above schema

#Insert data into the table

cursor.execute("INSERT INTO STUDENT VALUES('John', 20, 'New York', 85);")
cursor.execute("INSERT INTO STUDENT VALUES('Alice', 22, 'Los Angeles', 90);")
cursor.execute("INSERT INTO STUDENT VALUES('Bob', 21, 'Chicago', 75);")

#display the data in the table
print("Data in STUDENT table:")
data = cursor.execute("SELECT * FROM STUDENT;")
for row in data:
    print(row)