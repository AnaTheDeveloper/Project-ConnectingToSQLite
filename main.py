import sqlite3
import pandas as pd

# Create connection to database
connection = sqlite3.connect("first.db")

# we need a way to call SQL statements on the data within the database. A cursor object represents a database cursor,
# and can be used to call statements to our SQLite database, and return the data in our python environment.

# Create cursor object
cursor = connection.cursor()

# If we imagine the connection object as a cable that connects Python to SQLite, the cursor would use the cable
# to move back and forth to send messages and exchange data between the two.

# Create students table
cursor.execute('''CREATE TABLE students (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    major_code INTEGER,
                    grad_date datetime,
                    grade REAL NOT NULL)''')

# Add a row of data to students table
cursor.execute('''INSERT INTO students VALUES (101, 'Alex', 'alex@codeu.com', 32, '2022-05-16', 'Pass')''')

# Insert multiple values into table at once
students = [(102, 'Joe', 'joseph@codeu.com', 32, '2022-05-16', 'Pass'),
            (103, 'Stacy', 'stacy@codeu.com', 10, '2022-05-16', 'Pass'),
            (104, 'Angela', 'angela@codeu.com', 21, '2022-12-20', 'Pass'),
            (105, 'Mark', 'mark@codeu.com', 21, '2022-12-20', 'Fail'),
            (106, 'Nathan', 'nathaniel@codeu.com', 21, '2022-12-20', 'Pass')
            ]

# Insert values into the students table
cursor.executemany('''INSERT INTO students VALUES (?,?,?,?,?,?)''', students)

# Commit changes to database
connection.commit()

# Iterate through all rows in students table
for row in cursor.execute("SELECT * FROM students"):
    print(row)

# ----Terminal Output--------

# (101, 'Alex', 'alex@codeu.com', 32, '2022-05-16', 'Pass')
# (102, 'Joe', 'joseph@codeu.com', 32, '2022-05-16', 'Pass')
# (103, 'Stacy', 'stacy@codeu.com', 10, '2022-05-16', 'Pass')
# (104, 'Angela', 'angela@codeu.com', 21, '2022-12-20', 'Pass')
# (105, 'Mark', 'mark@codeu.com', 21, '2022-12-20', 'Fail')
# (106, 'Nathan', 'nathaniel@codeu.com', 21, '2022-12-20', 'Pass')

# Return first row in students
cursor.execute("SELECT * FROM students").fetchone()

# Return first three rows in students
cursor.execute("SELECT * FROM students").fetchmany(3)

# Return all rows in students
cursor.execute("SELECT * FROM students").fetchall()

# Notice that using for loops and the fetchone() method return tuples, while fetchmany() and fetchall() return lists of tuples.

# Return the number of rows with a passing grade
cursor.execute("""SELECT COUNT(*) FROM students WHERE Grade = 'Pass';""").fetchone()

# Find the average of the major codes field:

# Create a list of tuples of the major codes
major_codes = cursor.execute("SELECT major_code FROM students;").fetchall()

# Obtain the average of the tuple list by using for loops
sum = 0
for num in major_codes:
    for i in num:
        sum = sum + i
average = sum / len(major_codes)

# Show average
print(average)

# ---------Using SQLite with Pandas--------------------

# Create a new dataframe from the result set
df = pd.read_sql_query('''SELECT * from students;''', connection)
print(df)

# Want to create a DataFrame containing only those rows where the major code was equal to 21
df2 = pd.read_sql_query('''SELECT * from students WHERE major_code = 21;''', connection)
print(df2)

# Find the average of the major codes
df['major_code'].mean()
