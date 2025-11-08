import sqlite3
import os

# Remove existing database to start fresh
if os.path.exists("student.db"):
    os.remove("student.db")
# Create the database
connection = sqlite3.connect("student.db")
# Create a cursor
cursor = connection.cursor()
# Create the table
create_table_query="""
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME    VARCHAR(25),
    COURSE   VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS   INT
);
"""
cursor.execute(create_table_query)
# Insert Records
sql_query = """INSERT INTO STUDENT (NAME, COURSE, SECTION, MARKS) VALUES (?, ?, ?, ?)"""
values = [
    ('Abdullah', 'Data Science', 'A', 90),
    ('Dave', 'Data Science', 'B', 100),
    ('Super Men', 'Data Science', 'A', 86),
    ('Ali', 'DEVOPS', 'A', 50),
    ('Maryam', 'DEVOPS', 'A', 35)
]

cursor.executemany(sql_query, values)
connection.commit()

# Display the records
data=cursor.execute("""Select * from STUDENT""")

for row in data:
    print(row)

if connection:
    connection.close()