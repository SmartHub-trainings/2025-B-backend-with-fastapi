from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel,EmailStr
from sqlite3 import connect
from passlib.context import CryptContext
from dotenv import load_dotenv
import os 

load_dotenv()

DATABASE_NAME= os.getenv("DB_NAME")
# print(DATABASE_NAME)


pwd_context=CryptContext(schemes=["bcrypt"],
    deprecated="auto"
)


conn = connect(DATABASE_NAME)
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

cur.execute("""
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    venue VARCHAR(255) NOT NULL,
    date DATE DEFAULT current_date,
    time VARCHAR(20) NOT NULL,
    category VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    note TEXT  
)    
""")

# cur.execute("select * from events")
# print(cur.fetchall())


conn.commit()
conn.close()


class UserEmail(BaseModel):
    email:EmailStr

class UserUpdate(UserEmail):
    full_name:str
    phone_number:str
class UserCreate(UserUpdate):
    password:str
    confirm_password:str

class UserLogin(UserEmail):
    password:str
    
class EventCreate(BaseModel):
    title:str
    description:str
    date: str
    venue:str
    category:str
    time:str
    user_id:int

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

def connect_db():
    conn = connect("kickets.db")
    cur = conn.cursor()
    return conn,cur
    
    


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok",
    "timestamp":datetime.now()
    }

@app.post("/auth/register",tags=["Authentication"])
def register(payload:UserCreate):
    # print(payload)
    conn,cur = connect_db()
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
    _,cur = connect_db()
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




@app.get("/users")
def get_all_users():
    _,cur = connect_db()
    data = cur.execute("SELECT * FROM users").fetchall()
    users =[]
    for row in data:
        # print(row)
        user=format_user(row)
        users.append(user)
    return {"message": "all users",
        "data":users
    }

@app.get("/events",tags=["Events"])
def get_all_events():
    _,cur = connect_db()
    data =cur.execute("select * from events").fetchall()
    return {
        "message": "Events retrieved successfully",
        "success":True,
        "statusCode":200,
        "data":data
    }

@app.post("/events",tags=["Events"])
def create_event_handler(body:EventCreate):
    conn, cur = connect_db()
    event_row=cur.execute("""insert into 
    events(title,description, date,time, venue,user_id,category)
    values(?,?,?,?,?,?,?) 
    """,(body.title,body.description,body.date,body.time,body.venue,
    body.user_id,body.category))
    event =cur.execute("select * from events where event_id=?",
    (event_row.lastrowid,)).fetchone()
    if event:
        cur.execute("update users set role ='host' where user_id =?",
        (body.user_id,))

    conn.commit()
    conn.close()
    return {
        "message": "Events retrieved successfully",
        "success":True,
        "statusCode":200,
        "data":event
    }

