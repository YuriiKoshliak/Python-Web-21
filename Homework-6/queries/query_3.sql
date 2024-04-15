SELECT groups.name AS group_name, AVG(grades.grade) AS average_math_grade
FROM groups
JOIN students ON groups.id = students.group_id
JOIN grades ON students.id = grades.student_id
JOIN subjects ON grades.subject_id = subjects.id
WHERE subjects.name = 'Math'
GROUP BY groups.name;
