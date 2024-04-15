import sqlite3
from faker import Faker
import random

fake = Faker('uk_UA')

def adapt_date(date):
    return date.strftime('%Y-%m-%d')

def insert_groups(cursor, group_names):
    for group_name in group_names:
        cursor.execute('INSERT INTO groups (name) VALUES (?)', (group_name,))

def insert_teachers(cursor, teacher_names):
    for teacher_name in teacher_names:
        cursor.execute('INSERT INTO teachers (name) VALUES (?)', (teacher_name,))

def insert_subjects(cursor, subject_names):
    for subject_name in subject_names:
        teacher_id = random.randint(1, 5)
        cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', (subject_name, teacher_id))

def insert_students(cursor, num_students):
    for _ in range(num_students):
        group_id = random.randint(1, 3)
        student_name = fake.name()
        cursor.execute('INSERT INTO students (name, group_id) VALUES (?, ?)', (student_name, group_id))

def insert_grades(cursor, num_students):
    for student_id in range(1, num_students + 1):
        for _ in range(random.randint(10, 20)):
            subject_id = random.randint(1, 8)
            grade = random.randint(1, 10)
            date_received = adapt_date(fake.date_between(start_date='-1y', end_date='today'))
            cursor.execute('INSERT INTO grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?)',
                           (student_id, subject_id, grade, date_received))

def insert_all_data():
    with sqlite3.connect('school.db') as conn:
        cursor = conn.cursor()
        insert_groups(cursor, ['A', 'B', 'C'])
        insert_teachers(cursor, [fake.name() for _ in range(5)])
        insert_subjects(cursor, ['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'English', 'Programming'])
        insert_students(cursor, 50)
        insert_grades(cursor, 50)

if __name__ == '__main__':
    insert_all_data()
