from typing import List

from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email:str
    password:str

class Users(UserCreate):
    id: int
    class Config:
        orm_mode = True

class LisansCreate(BaseModel):
    musterikodu: str
    dbname:str
    dbusername:str
    dbpassword:str

class lisans(LisansCreate):
    id: int
    class Config:
        orm_mode = True


class OrtakCreate(BaseModel):
    musterikodu: str
    userdb:str

class ortak(OrtakCreate):
    id: int
    class Config:
        orm_mode = True

class Login(BaseModel):
    musterikodu: str
    email:str
    password:str