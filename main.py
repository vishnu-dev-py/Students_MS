from fastapi import FastAPI, Body
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn


import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="con1?vex",
    database="sms"
    )

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware, allow_origins=['*'], allow_methods = ['*']
    )

@app.post("/create_student")
async def create_student(student_details:Dict = Body(...)):
    student_details = jsonable_encoder(student_details)
    try:
        cursor = connection.cursor()
        statement = "insert into student (name,age,department) values('{}',{},'{}')".format(student_details['name'], student_details['age'], student_details['department'])
        cursor.execute(statement)
        connection.commit()
        return "Student '{}' Created".format(student_details['name'])

    except Exception as e:
        return "Student not created"


@app.post("/update_student")
async def update_student(student_details:Dict = Body(...)):
    student_details = jsonable_encoder(student_details)
    try:
        cursor = connection.cursor()
        statement = "update student set age = {}, department = '{}', name = '{}' where rollno = {}".format(student_details['age'], student_details['department'],student_details['name'],student_details['roll_no'])
        print(statement)
        cursor.execute(statement)
        connection.commit()
        return "Student '{}' Updated!".format(student_details['name'])

    except Exception as e:
        return e


@app.get("/delete_student/{id}")
async def delete_student(id):
    try:
        cursor = connection.cursor()
        statement = "delete from student where rollno = {}".format(int(id))
        cursor.execute(statement)
        connection.commit()
        return "Student {} deleted!".format(id)
    except Exception as e:
        return e

@app.get("/get_student/{id}")
async def get_student(id):
    try:
        cursor = connection.cursor()
        if int(id) == -1:
            statement = "select * from student"
            cursor.execute(statement)
            rows = cursor.fetchall()

            students = []
            for row in rows:
                students.append(dict(zip(['roll_no', 'name', 'age', 'department'], row)))
            return students
        else:

            statement = "select * from student where rollno = {}".format(int(id))
            cursor.execute(statement)
            student = cursor.fetchone()

            if student:
                return dict(zip(['roll_no', 'name', 'age', 'department'], student))
            else:
                return "Student not found"
    except Exception as e:
        return "Something went wrong"


if __name__ == "__main__":
    uvicorn.run(
        "main:app"
    )

