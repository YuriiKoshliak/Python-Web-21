SELECT students.name, grades.grade
FROM grades
JOIN students ON grades.student_id = students.id
JOIN groups ON students.group_id = groups.id
JOIN subjects ON grades.subject_id = subjects.id
WHERE groups.id = 1  AND subjects.id = 2
AND grades.date_received = (
    SELECT MAX(grades.date_received)
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN groups ON students.group_id = groups.id
    JOIN subjects ON grades.subject_id = subjects.id
    WHERE groups.id = 1 AND subjects.id = 2
)
