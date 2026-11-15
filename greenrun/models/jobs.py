"""
jobs.py

contains database queries for logging jobs and their scheduled/immediate intensities
"""


def insert_job(conn, **fields):
    columns = ", ".join(fields)
    marks = ", ".join("?" * len(fields))
    cursor = conn.execute(f"INSERT INTO jobs({columns})) VALUES ({marks})", tuple(fields.values()))
    conn.commit()
    return cursor.lastrowid

def update_job(conn, job_id, **fields):
    assignments = ", ".join(f"{name} = ?" for name in fields)
    conn.execute(f"UPDATE jobs SET {assignments} WHERE id = ?", (*fields.values(), job_id))
    conn.commit()