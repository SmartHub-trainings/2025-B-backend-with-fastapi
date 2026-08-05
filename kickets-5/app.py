from fastapi import Depends,FastAPI
from datetime import datetime
from pydantic import BaseModel,EmailStr
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from dotenv import load_dotenv
import os 
from sqlalchemy import create_engine,Column,Integer,String,DateTime,Date,ForeignKey,select
from sqlalchemy.orm import sessionmaker,DeclarativeBase,Session

load_dotenv()

DATABASE_URL= os.getenv("DB_URL")
# print(DATABASE_URL)

engine = create_engine(DATABASE_URL,
connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def get_db():
    db=SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        print("Database Error")
    finally:
        db.close()




class User(Base):
    __tablename__="users"

    user_id = Column(Integer,primary_key=True)
    email = Column(String,nullable=False,unique=True)
    first_name =Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    phone_number = Column(String,nullable=False)
    password = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())
    role = Column(String,default="user")

class Event(Base):
    __tablename__="events"

    event_id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False)
    description = Column(String,nullable=False)
    date = Column(Date,default=datetime.now().date())
    time = Column(String,nullable=False)
    venue = Column(String,nullable=False)
    category = Column(String,nullable=False)
    created_at = Column(DateTime,default=datetime.now())
    updated_at = Column(DateTime,default=datetime.now())
    user_id = Column(Integer,ForeignKey("users.user_id"),nullable=False)
    note = Column(String)

Base.metadata.create_all(bind=engine)


pwd_context=CryptContext(schemes=["bcrypt"],
    deprecated="auto"
)

## seed an admin to the db
def seed_admin():
    db=SessionLocal()
    user = User(
            email="gbs@gmail.com",
            first_name="Admin",
            last_name="User",
            phone_number="0123456789",
            password=pwd_context.hash("password"),
            role="admin"
        )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

# seed_admin()


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
        "id":row.user_id,
        "email":row.email,
        "first_name":row.first_name,
        "last_name":row.last_name,
        "phone_number":row.phone_number,
        "created_at":row.created_at,
        "updated_at":row.updated_at,
        "role":row.role
    }


    
    


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok",
    "timestamp":datetime.now()
    }

@app.post("/auth/register",tags=["Authentication"])
def register(payload:UserCreate):
    
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
def login_user(payload:UserLogin,db:Session = Depends(get_db)):
    email = payload.email
    password = payload.password
    # user =db.query(User).filter(User.email==email).first()
    # user =db.get(User,3)
    query = select(User).where(User.email==email)
    user = db.execute(query).scalar_one()
    print(user)

    # query = select(User).limit(2).offset(3)
    # users = db.execute(query).all()
    # print(users)

    # print(user)
    if not user:
        return {
            "message":"Invalid credientails",
            "success":False,
            "statusCode":401
        }
    is_password = pwd_context.verify(password,user.password)
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
def get_all_users(db=Depends(get_db)):
    data =db.query(User).all()
    return {"message": "all users",
        "data":data
    }

@app.get("/events",tags=["Events"])
def get_all_events(db:Session =Depends(get_db)):
    data =db.query(Event).all()
    return {
        "message": "Events retrieved successfully",
        "success":True,
        "statusCode":200,
        "data":data
    }

@app.post("/events",tags=["Events"])
def create_event_handler(body:EventCreate,db:Session= Depends(get_db)):

    try:

        event= Event(
            title=body.title,
            description=body.description,
            date=datetime.strptime(body.date, "%Y-%m-%d").date(),
            time=body.time,
            venue=body.venue,
            user_id=body.user_id,
            category=body.category
        )

        db.add(event)
        db.commit()
        db.refresh(event)
        if event:
            query = select(User).where(User.user_id==body.user_id)
            user = db.execute(query).scalar_one()
            if user.role != "host":
                user.role = "host"
                db.commit()
                db.refresh(user)

        return {
            "message": "Events created successfully",
            "success":True,
            "statusCode":200,
            "data":event
        }
    except Exception as e:
        print(e)
        return {
            "message": "Events retrieved failed",
            "success":False,
            "statusCode":400
        }

