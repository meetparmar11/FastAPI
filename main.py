from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import engine, SessionLocal
from models import Base, Student

# Create FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Static files folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder
templates = Jinja2Templates(directory="templates")


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "FastAPI Project"
        }
    )


# Path Parameter Example
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "query": q
    }


# Get All Students
@app.get("/students")
def get_students():
    db = SessionLocal()

    try:
        students = db.query(Student).all()

        return [
            {
                "id": student.id,
                "name": student.name,
                "age": student.age
            }
            for student in students
        ]

    finally:
        db.close()


# Get Student by ID
@app.get("/students/{student_id}")
def get_student(student_id: int):
    db = SessionLocal()

    try:
        student = db.query(Student).filter(
            Student.id == student_id
        ).first()

        if not student:
            return {"message": "Student not found"}

        return {
            "id": student.id,
            " name": student.name,
            "age": student.age
        }

    finally:
        db.close()


    