from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional

app =FastAPI()

class UserRegister(BaseModel):
    email: str
    first_name: str=Field(..., min_length=3, max_length=10)
    last_name: Optional[str]=None
    password: str
    confirm_password: str
    age :int

class Course(BaseModel):
    title: str
    description: Optional[str]=None
    price: float
    instructor: Optional[str]=None

users =[
    {"id":1,
    "name":"Kosi",
    "email":"kosi@gmail.com",
    "isMarried":True},
    {"id":2,
    "name":"Best",
    "email":"best@gmail.com",
    "isMarried":False},
    {"id":3,
    "name":"Gideon",
    "email":"gideon@gmail.com",
    "isMarried":True},
    {"id":5,
    "name":"James",
    "email":"james@gmail.com",
    "isMarried":True},
    {"id":6,
    "name":"Great",
    "email":"great@gmail.com",
    "isMarried":True}
]

courses= []

@app.get("/students")
def get_all_students():
    return {
        "statusCode":200,
        "message":"Retrieved all users",
        "success":True,
        "data":users
    }


@app.get("/students/{id}")
def get_a_student_by_id(id:int):
    
    for user in users:
        if user["id"] == id:
            return {
                "statusCode":200,
                "message":"Retrieved  user details",
                "success":True,
                "data":user
            }
    return {
        "statusCode":404,
        "message":"User not found.",
        "success":False
    }


@app.post("/students")
def create_new_student(payload:dict):
    print(payload)
    for a_user in users:
        if a_user["email"]==payload["email"]:
            return {
                "message":"User with this email already exists",
                "statusCode":409,
                "success":False
            }
    user= payload
    user_id = users[-1]["id"]+1
    print(user_id)
    user["id"]=user_id
    users.append(user)

    return {
        "message":"Student created successfully",
        "statusCode":201,
        "success":True,
        "data":user
    }

@app.delete("/students/{id}")
def delete_student(id:int):
    for user in users:
        if user["id"]==id:
            users.remove(user)
            return {
                "message":"User deleted successfully",
                "statusCode":200,
                "success":True
            }
    return {
        "statusCode":404,
        "message":"User not found.",
        "success":False
    }

@app.put("/students/{id}")
def update_student(id:int,payload:dict):
    for user in users:
        # print({"user":user,"payload":payload})
        if user["id"]==id:
            user.update(payload)
            return {
                "message":"User updated successfully",
                "statusCode":200,
                "success":True,
                "data":user
            }
    return {
        "message":"User not found",
        "statusCode":404,
        "success":False
    }

## courses endpoints 
@app.get("/courses")
def get_all_courses():
    return{
        "statusCode":200,
        "message":"Retrieved all courses",
        "success":True,
        "data":courses
    }

@app.post("/courses")
def create_new_course(payload:Course):
    course = payload
    course["id"] = 1 if len(courses)==0 else courses[-1]["id"]+1
    courses.append(course)
    return {
        "message":"Course created successfully",
        "statusCode":201,
        "success":True,
        "data":course
    }



@app.post("/students/register")
def student_register(payload:UserRegister):
    print(payload)

    
    # if payload["password"] != payload["confirm_password"]:
    #     return {
    #         "message":"Password and confirm password must match",
    #         "statusCode":400,
    #         "success":False
    #     }

    return {
        "message":"Registration successful",
        "statusCode":201,
        "success":True,
        "data":payload
    }
    


    

