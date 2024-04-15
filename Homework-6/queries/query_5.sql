SELECT teachers.name AS teacher_name, GROUP_CONCAT(subjects.name) AS subjects_taught
FROM teachers
JOIN subjects ON teachers.id = subjects.teacher_id
GROUP BY teachers.id;
