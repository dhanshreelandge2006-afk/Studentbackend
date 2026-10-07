from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port= os.getenv('DB_PORT'),
    database=os.getenv('DB_DATABASE'),
    user=os.getenv('DB_USER'),
    password= os.getenv('DB_PASSWORD')
)

cursor = connection.cursor()


class Student(BaseModel):
    id: int=None
    name: str=None
    course: str=None


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
@app.get('/students/{id}')
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
        raise HTTPException(
            status_code=500,
            detail="student id already exists"
        )
#update sttudent record
@app.put('/students/{id}')
def update_student_record(id:int,student:Student):
    cursor.execute("update students SET id=%s,name=%s,course=%s where id=%s",(student.id,student.name,student.course,id))
    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail="invalid id")
    connection.commit()
    raise HTTPException(status_code=200,detail="student record updated successfully")

#partial update 
@app.patch('/students/{id}')
def partial_update(id:int,student:Student):
    if(student.id !=None):
        cursor.execute("update students set id=%s where id=%s",(student.id,id))
    if(student.name !=None):
        cursor.execute("update students set name=%s where id=%s",(student.name,id))
    if(student.course !=None):
        cursor.execute("update students set course=%s where id=%s",(student.course,id))
    if(cursor.rowcount==0):
        raise HTTPException(status_code=404,detail="invali id")
    connection.commit()
    raise HTTPException(status_Code=200,detail="partial update successfully")
@app.delete('/students/{id}')
def delete_student(id: int):
       cursor.execute("DELETE FROM students WHERE id=%s", (id,))
       if cursor.rowcount == 0:
         raise HTTPException(status_code=404, detail="Invalid student id")
       connection.commit()
       raise HTTPException(status_code=200,detail="record deleted successfully")