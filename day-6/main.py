import email
from fastapi import FastAPI

app =FastAPI()
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
def create_new_course(payload:dict):
    course = payload
    course["id"] = 1 if len(courses)==0 else courses[-1]["id"]+1
    courses.append(course)
    return {
        "message":"Course created successfully",
        "statusCode":201,
        "success":True,
        "data":course
    }

# @app.post("/students/register")
# def student_register(payload:dict):
#     print(payload)
#     # print(payload.get("email","missing"))
#     if not payload.get("email"):
#         return {
#             "message":"Email is required",
#             "statusCode":400,
#             "success":False
#         }
    
#     if not payload.get("first_name"):
#         return {
#             "message":"First name is required",
#             "statusCode":400,
#             "success":False
#         }
    
#     if not payload.get("last_name"):
#         return {
#             "message":"Last name is required",
#             "statusCode":400,
#             "success":False
#         }
    
#     if not payload.get("password"):
#         return {
#             "message":"Password is required",
#             "statusCode":400,
#             "success":False
#         }
    
#     if not payload.get("confirm_password"):
#         return {
#             "message":"Confirm password is required",
#             "statusCode":400,
#             "success":False
#         }
        
#     is_valid_email = "@" in payload["email"]
#     if not is_valid_email:
#         return {
#             "message":"Invalid email",
#             "statusCode":400,
#             "success":False
#         }

#     if len(payload["first_name"])<3:
#         return {
#             "message":"First name should have atleast 3 characters",
#             "statusCode":400,
#             "success":False
#         }
    
#     if len(payload["last_name"])<3:
#         return {
#             "message":"Last name should have atleast 3 characters",
#             "statusCode":400,
#             "success":False
#         }
    
#     if len(payload["password"])<8:
#         return {
#             "message":"Password should have atleast 8 characters",
#             "statusCode":400,
#             "success":False
#         }
    
#     if payload["password"] != payload["confirm_password"]:
#         return {
#             "message":"Password and confirm password must match",
#             "statusCode":400,
#             "success":False
#         }

#     return {
#         "message":"Registration successful",
#         "statusCode":201,
#         "success":True,
#         "data":payload
#     }
    


    # is_valid_first_name = len(payload["first_name"])
    # is_valid_last_name = len(payload["last_name"])
    # is_valid_password = len(payload["password"])
    # is_valid_confirm_password = payload["confirm_password"]
    

    # email: follows email format 
    # first name: should have atleast 3 characters 
    # last name: should have atleast 3 characters 
    # password: should have atleast 8 characters, 1 upper case and a special character 
    # confirm password: should match the password
    


# create endpoint to delete a course by id 

# create endpoint to get a course by id 

# create endpoint to update a course by id


@app.post("/students/register")
def student_register(payload:dict):
    print(payload)
    required_fields =["email","first_name","last_name","password","confirm_password"]

    for field in required_fields:
        if not payload.get(field):
            return {
                "message":f"{field} is required",
                "statusCode":400,
                "success":False
            }

    is_valid_email = "@" in payload["email"]
    if not is_valid_email:
        return {
            "message":"Invalid email",
            "statusCode":400,
            "success":False
        }

    if len(payload["first_name"])<3:
        return {
            "message":"First name should have atleast 3 characters",
            "statusCode":400,
            "success":False
        }
    
    if len(payload["last_name"])<3:
        return {
            "message":"Last name should have atleast 3 characters",
            "statusCode":400,
            "success":False
        }
    
    if len(payload["password"])<8:
        return {
            "message":"Password should have atleast 8 characters",
            "statusCode":400,
            "success":False
        }
    
    if payload["password"] != payload["confirm_password"]:
        return {
            "message":"Password and confirm password must match",
            "statusCode":400,
            "success":False
        }

    return {
        "message":"Registration successful",
        "statusCode":201,
        "success":True,
        "data":payload
    }
    


    

