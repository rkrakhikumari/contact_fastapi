from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name : str
    email : str
    password : str



class UserLogin(BaseModel):
    name : str
    password : str


class ContactCreate(BaseModel):
    name : str = Field(min_length=3)
    email : str 
    phone_num : str
    note : str