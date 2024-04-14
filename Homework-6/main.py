import sqlite3
from faker import Faker
import random
import datetime

fake = Faker('uk_UA')

# Function to convert date to string format for SQLite
def adapt_date(date):
    return date.strftime('%Y-%m-%d')

with sqlite3.connect('school.db') as conn:
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        group_id INTEGER,
        FOREIGN KEY (group_id) REFERENCES groups(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        date_received DATE,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
    ''')

    group_names = ['A', 'B', 'C']
    for group_name in group_names:
        cursor.execute('INSERT INTO groups (name) VALUES (?)', (group_name,))

    teacher_names = [fake.name() for _ in range(5)]
    for teacher_name in teacher_names:
        cursor.execute('INSERT INTO teachers (name) VALUES (?)', (teacher_name,))

    subject_names = ['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'English', 'Programming']
    for subject_name in subject_names:
        teacher_id = random.randint(1, 5)
        cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', (subject_name, teacher_id))

    for _ in range(50):
        group_id = random.randint(1, 3)
        student_name = fake.name()
        cursor.execute('INSERT INTO students (name, group_id) VALUES (?, ?)', (student_name, group_id))

    for student_id in range(1, 51):
        for _ in range(random.randint(10, 20)):
            subject_id = random.randint(1, 8)
            grade = random.randint(1, 10)
            date_received = adapt_date(fake.date_between(start_date='-1y', end_date='today'))
            cursor.execute('INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?)',
                           (student_id, subject_id, grade, date_received))
