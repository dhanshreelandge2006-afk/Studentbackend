from fastapi import FastAPI,HTTPException
import psycopg2 
app=FastAPI()
connection=psycopg2.connect(
    host='localhost',
    port='5432',
    database='postgres',
    user='postgres',
    password='postgress'
)
cursor=connection.cursor()
#get all studenets
@app.get('/students')
def get_all_students():
    cursor.execute("select * from students")
    rows=cursor.fetchall()

    result=[]
    for row in rows:
        result.append({
            'id':row[0],
            'name':row[1],
            'course':row[2]
        })
    return result
#get single student
@app.get('/students/{id}') #fast api variable  
def get_single_student(id:int):
    try:
        cursor.execute("select * from students  where id=%s", (id,))
        row=cursor.fetchone()
        return{
            "id":row[0],
            "name":row[1],
            "course":row[2]
        }
    except:
        raise HTTPException(status_code=404,detail="invalid Student id ")