from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    # email:str
    email:EmailStr
    password:str
    full_name:str
    phone_number:str
    confirm_password:str
    


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok",
    "timestamp":datetime.now()
    }

@app.post("/auth/register")
def register(payload:UserCreate):
    print(payload)
    first_name,last_name = payload.full_name.split(" ")
    print("first_name",first_name)
    print("last_name",last_name)

    return {"message": "register",
        "data":payload
    }
    
    