import sqlite3
from datetime import datetime
import pandas as pd

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_student_to_db(student_id, name):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO students (id, name) VALUES (?, ?)", (student_id, name))
    conn.commit()
    conn.close()

def delete_student_from_db(student_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    rows = c.fetchall()
    conn.close()
    return rows

def mark_attendance(name):
    file = "attendance.csv"
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    try:
        df = pd.read_csv(file)
        # ✅ Check if required columns exist
        if not {"Name", "Date", "Time"}.issubset(df.columns):
            raise ValueError("Invalid CSV format. Rebuilding file.")
    except (FileNotFoundError, ValueError):
        # ✅ Create new DataFrame with correct structure
        df = pd.DataFrame(columns=["Name", "Date", "Time"])

    # ✅ Only mark if student not already marked today
    if not ((df["Name"] == name) & (df["Date"] == date_str)).any():
        new_entry = pd.DataFrame({"Name": [name], "Date": [date_str], "Time": [time_str]})
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(file, index=False)