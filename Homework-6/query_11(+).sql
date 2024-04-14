SELECT AVG(grades.grade) AS average_grade
FROM grades
JOIN subjects ON grades.subject_id = subjects.id
JOIN teachers ON subjects.teacher_id = teachers.id
WHERE teachers.id = 1 AND grades.student_id = 3;
