from fastapi import FastAPI, HTTPException
import psycopg2
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# connection = psycopg2.connect(
#     host=os.getenv('DB_HOST'),
#     port= os.getenv('DB_PORT'),
#     database=os.getenv('DB_DATABASE'),
#     user=os.getenv('DB_USER'),
#     password= os.getenv('DB_PASSWORD')
# )

connection=psycopg2.connect("postgresql://neondb_owner:npg_LhqCE5ro2kQO@ep-summer-hat-b3sgcv74-pooler.c-4.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")


class Student(BaseModel):
    id: int=None
    name: str=None
    course: str=None


# get all students
@app.get('/students')
def get_all_students():
    cursor = connection.cursor()

    cursor.execute("select * from students")
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            'id': row[0],
            'name': row[1],
            'course': row[2]
        })
    cursor.close()
    return result


# get single student
@app.get('/students/{id}')
def get_single_student(id: int):
    try:
        cursor = connection.cursor()
        cursor.execute("select * from students where id=%s", (id,))
        row = cursor.fetchone()
        cursor.close()
        return {
            "id": row[0],
            "name": row[1],
            "course": row[2]
        }

    except:
        cursor.close()
        raise HTTPException(status_code=404, detail="invalid Student id")


# create student record
@app.post('/students')
def create_student_records(student: Student):
    try:
        cursor = connection.cursor()
        cursor.execute(
            "insert into students values(%s, %s, %s)",
            (student.id, student.name, student.course)
        )
        connection.commit()
        cursor.close()
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
    cursor = connection.cursor()
    cursor.execute("update students SET id=%s,name=%s,course=%s where id=%s",(student.id,student.name,student.course,id))
    if(cursor.rowcount==0):
        cursor.close()
        raise HTTPException(status_code=404,detail="invalid id")
    connection.commit()
    cursor.close()
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
       cursor = connection.cursor()
       cursor.execute("DELETE FROM students WHERE id=%s", (id,))
       if cursor.rowcount == 0:
         raise HTTPException(status_code=404, detail="Invalid student id")
       connection.commit()
       cursor.close()
       raise HTTPException(status_code=200,detail="record deleted successfully")