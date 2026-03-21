import sqlite3

# Build connection
connection = sqlite3.connect("mystudents.db")

cursor = connection.cursor()

# Create table
table_info = '''
CREATE TABLE IF NOT EXISTS STUDENTS(
id INTEGER PRIMARY KEY AUTOINCREMENT,
NAME TEXT NOT NULL,
GENDER TEXT,
AGE INT,
Date_of_birth DATE,
MARKS REAL,
Subject TEXT,
City TEXT
)
'''

cursor.execute(table_info)

# Insert records
cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('Mahi', 'Male', 22, '2003-12-07', 9.8, 'Gen AI', 'Hyderabad')
""")

cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('Sam', 'Male', 22, '2004-12-12', 9.1, 'Devops', 'Bangalore')
""")

cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('Tony', 'Male', 23, '2003-11-04', 8.8, 'Cybersecurity', 'Delhi')
""")

cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('Rani', 'Female', 24, '2003-01-06', 7.8, 'ML Engineer', 'Mumbai')
""")

cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('John', 'Male', 21, '2004-02-07', 8.7, 'Data Science', 'Bengal')
""")
cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('Mari', 'Female', 22, '2004-02-07', 8.7, 'Data Science', 'Hyderabad')
""")
cursor.execute("""
INSERT INTO STUDENTS (NAME, GENDER, AGE, Date_of_birth, MARKS, Subject, City)
VALUES ('Rahul', 'Male', 21, '2006-07-02', 7.7, 'Machine Learning', 'Chennai')
""")

connection.commit()

print("The inserted records are:")

data = cursor.execute("SELECT * FROM STUDENTS")

for row in data:
    print(row)

connection.close()