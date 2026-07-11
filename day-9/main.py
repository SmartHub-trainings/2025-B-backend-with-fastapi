from fastapi import FastAPI
from pydantic import BaseModel,Field,EmailStr,model_validator
from typing import Optional
from sqlite3 import connect




# cursor.execute("""
#  CREATE TABLE courses (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     title TEXT NOT NULL,
#     description TEXT,
#     price REAL NOT NULL,
#     instructor TEXT
# );
# """)

# courses = cursor.execute("select * from courses").fetchall()
# print(courses)
app =FastAPI()

class UserRegister(BaseModel):
    email: EmailStr
    first_name: str=Field(..., min_length=3, max_length=10)
    last_name: Optional[str]=None
    password: str
    confirm_password: str
    age :int= Field(..., gt=16,le=100)


    @model_validator(mode="after")
    def confirm_password(self):
        print("In validator",self)
        if self.password != self.confirm_password:
            raise ValueError("Passwords must be best")
        # return self

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



@app.get("/students",tags=["students"])
def get_all_students():
    return {
        "statusCode":200,
        "message":"Retrieved all users",
        "success":True,
        "data":users
    }


@app.get("/students/{id}",tags=["students"])
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


@app.post("/students",tags=["students"])
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

@app.delete("/students/{id}",tags=["students"])
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

@app.put("/students/{id}",tags=["students"])
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
@app.get("/courses",tags=["courses"])
def get_all_courses():
    conn= connect("best_college.db")
    cursor=conn.cursor()
    courses = cursor.execute("select * from courses").fetchall()
    formated_courses = []
    for course in courses:
        formated_course= {
            "id":course[0],
            "title":course[1],
            "description":course[2],
            "price":course[3],
            "instructor":course[4]
        }
        formated_courses.append(formated_course)
    return{
        "statusCode":200,
        "message":"Retrieved all courses",
        "success":True,
        "data":formated_courses
    }

@app.post("/courses",tags=["courses"])
def create_new_course(payload:Course):
    course = payload
    conn = connect("best_college.db")
    cursor=conn.cursor()
    new_course= cursor.execute("""
    INSERT INTO courses (title,description,price,instructor) VALUES (?,?,?,?)
    """,(course.title,course.description,course.price,course.instructor))
    conn.commit()
    
    print(new_course.lastrowid)
    new_course = cursor.execute("""select * from courses where id = ?""",
    (new_course.lastrowid,)).fetchone()
    #  [
    #   1,
    #   "Data Science",
    #   "A cool way predicting the future",
    #   5000,
    #   "Mr. Vic"
    # ]
    formated_course= {
        "id":new_course[0],
        "title":new_course[1],
        "description":new_course[2],
        "price":new_course[3],
        "instructor":new_course[4]
    }
    conn.close()
    return {
        "message":"Course created successfully",
        "statusCode":201,
        "success":True,
        "data":formated_course
    }



@app.post("/students/register",tags=["students"])
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
    


    

