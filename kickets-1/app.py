from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel,EmailStr
from sqlite3 import connect
from passlib.context import CryptContext


pwd_context=CryptContext(schemes=["bcrypt"],
    deprecated="auto"
)


conn = connect("kickets.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(10) NOT NULL DEFAULT 'user'
)    
""")


conn.commit()
conn.close()

class UserCreate(BaseModel):
    # email:str
    email:EmailStr
    password:str
    full_name:str
    phone_number:str
    confirm_password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

def format_user(row):
    return {
        "id":row[0],
        "email":row[1],
        "first_name":row[2],
        "last_name":row[3],
        "phone_number":row[4],
        "created_at":row[6],
        "updated_at":row[7],
        "role":row[8]
    }
    
    


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok",
    "timestamp":datetime.now()
    }

@app.post("/auth/register",tags=["Authentication"])
def register(payload:UserCreate):
    # print(payload)
    conn = connect("kickets.db")
    cur = conn.cursor()
    first_name,last_name = payload.full_name.split(" ")
    password = payload.password
    confirm_password = payload.confirm_password
    if password != confirm_password:
        return {
            "message":"passwords do not match",
            "success":False,
            "statusCode":400
        }
    # print("first_name",first_name)
    # print("last_name",last_name)
    saved_row=cur.execute("""
    INSERT INTO users (email,first_name,last_name,phone_number,password)
    VALUES (?,?,?,?,?)
    """,(payload.email,first_name,last_name,payload.phone_number,pwd_context.hash(payload.password)))
    conn.commit()
    row_id = saved_row.lastrowid
    print("row_id",row_id)
    conn.close()

    return {"message": "register",
        "data":payload
    }

@app.post("/auth/login",tags=["Authentication"])
def login_user(payload:UserLogin):
    conn = connect("kickets.db")
    cur = conn.cursor()
    email = payload.email
    password = payload.password
    user = cur.execute("select * from users where email=?",(email,)).fetchone()
    if not user:
        return {
            "message":"Invalid credientails",
            "success":False,
            "statusCode":401
        }
    is_password = pwd_context.verify(password,user[5])
    if not is_password:
        return {
            "message":"Invalid credientails",
            "success":False,
            "statusCode":401
        }

        
    return {
        "message": "user login",
        "success":True,
        "statusCode":200,
        "data":format_user(user)
    }


def connect_db():
    conn = connect("kickets.db")
    cur = conn.cursor()
    return conn,cur

@app.get("/users")
def get_all_users():
    conn = connect("kickets.db")
    cur = conn.cursor()
    data = cur.execute("SELECT * FROM users").fetchall()
    users =[]
    for row in data:
        # print(row)
        user=format_user(row)
        users.append(user)
    return {"message": "all users",
        "data":users
    }