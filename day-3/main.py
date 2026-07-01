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

@app.get("/students")
def get_all_students():
    return {
        "statusCode":200,
        "message":"Retrieved all users",
        "success":True,
        "data":users
    }

# @app.get("/students/{id}")
# def get_a_student_by_id(id:int):
#     # user = users[int(id)-1]
#     user = users[id-1]
    
#     return {
#         "statusCode":200,
#         "message":"Retrieved  user details",
#         "success":True,
#         "data":user
#     } 


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
    
    

