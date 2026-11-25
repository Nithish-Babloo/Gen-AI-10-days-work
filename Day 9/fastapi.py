
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Student data stored in memory
students = {
    1: {"name": "Ravi", "age": 21},
    2: {"name": "Priya", "age": 22}
}

# Request body model
class Student(BaseModel):
    name: str
    age: int


# GET API - Display all students
@app.get("/")
def home():
    return {"message": "Welcome to Student API"}


@app.get("/students")
def get_students():
    return students


# POST API - Add a new student
@app.post("/students/{student_id}")
def create_student(student_id: int, student: Student):

    if student_id in students:
        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    students[student_id] = student.model_dump()

    return {
        "message": "Student created successfully",
        "student": students[student_id]
    }


# PUT API - Update an existing student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):

    if student_id not in students:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    students[student_id] = student.model_dump()

    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }
