import sqlite3

## Connect to sqlite3
connection = sqlite3.connect("student.db")

## Create a cursor object to insert record,create table

cursor = connection.cursor()

## Create a Table
table_info = """
CREATE TABLE STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)
"""

cursor.execute(table_info)

## Insert some more Records
# Insert multiple records
records = [
    ('Rahul', 'TY-AIDS', 'B', 78),
    ('Sneha', 'TY-AIDS', 'A', 92),
    ('Amit', 'TY-AIDS', 'C', 67),
    ('Neha', 'TY-AIDS', 'B', 88)
]

cursor.executemany("""
INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS)
VALUES (?, ?, ?, ?)
""", records)

## Display all the records
print("The inserted records are")
data = cursor.execute("""SELECT * FROM STUDENT""")
for row in data:
    print(row)

## Commit your changes in the Database
connection.commit()
connection.close()
