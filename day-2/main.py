from fastapi import FastAPI

app =FastAPI()

@app.get("/students")
def get_all_students():
    return "I have given you all that i have"

@app.get("/students/{id}")
def get_a_student_by_id(id):
    return f"I will get you that student with id {id}."

