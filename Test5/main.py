import sqlite3


insert_query = "INSERT INTO jobs(id) VALUES(1)"
update_query = "UPDATE jobs SET id=2 WHERE id=1"

select_query = "SELECT COUNT(*) FROM jobs"

with sqlite3.connect("example.db") as conn:
    cursor = conn.cursor()

    cursor.execute(select_query)

    print(cursor.fetchone())

