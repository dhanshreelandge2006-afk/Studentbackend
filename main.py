from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel

app = FastAPI()

connection = psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password='postgress'
)

cursor = connection.cursor()


class Student(BaseModel):
    id: int
    name: str
    course: str


# get all students
@app.get('/students')
def get_all_students():
    cursor.execute("select * from students")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'id': row[0],
            'name': row[1],
            'course': row[2]
        })

    return result


# get single student
@app.get('/students/{id}')  # fast api variable
def get_single_student(id: int):
    try:
        cursor.execute("select * from students where id=%s", (id,))
        row = cursor.fetchone()

        return {
            "id": row[0],
            "name": row[1],
            "course": row[2]
        }

    except:
        raise HTTPException(status_code=404, detail="invalid Student id")


# create student record
@app.post('/students')
def create_student_records(student: Student):
    try:
        cursor.execute(
            "insert into students values(%s, %s, %s)",
            (student.id, student.name, student.course)
        )
        connection.commit()

        raise HTTPException(
            status_code=201,
            detail="student record created successfully"
        )
    except psycopg2.IntegrityError:
        connection.rollback()
        raise HTTPException(status_code=500 detail="student id already exists")