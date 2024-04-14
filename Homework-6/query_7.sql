SELECT students.name, grades.grade
FROM students
JOIN grades ON students.id = grades.student_id
JOIN groups ON students.group_id = groups.id
JOIN subjects ON grades.subject_id = subjects.id
WHERE groups.name = 'A' AND subjects.name = 'Math';
