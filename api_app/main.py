from typing import Optional,List
from . import crud, models, schemas,database_Lisans,database_Ortak
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database_Lisans import SessionLocal as SessionLocal_Lisans
from .database_Lisans import engine as enginel_Lisans
from .database_Ortak import SessionLocal as SessionLocal_Ortak
from .database_Ortak import engine as enginel_Ortak
import secrets
import requests
import json
from starlette.requests import Request
from starlette.responses import Response
import response
from pydantic import BaseModel
from jsonify import convert
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float, Numeric, MetaData, Table

from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
security = HTTPBasic()

# Dependency

def get_db_Lisans():
    try:
        db = SessionLocal_Lisans()
        yield db
    finally:
        db.close()

def get_db_Ortak():
    try:
        db = SessionLocal_Ortak()
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Merhaba": "Arzu"}


#Drop Database 
@app.post("/dropDB/")
def drop_db(dbname:str):
    drop_database = crud.drop_database(dbname=dbname)
    if(drop_database==1):
        return {'Sonuc':'Silindi'}
    else:
        return  {'Sonuc':'Hay aksi'}


#User List
@app.post("/kayit/")
def sign_up(user:schemas.UserCreate):
    kayit = crud.kayit(user=user)
    if(kayit==1):
        return {'Sonuc':'İşlem başarılı'}
    else:
        return  {'Sonuc':'Hay aksi'}

#User List
@app.post("/giris/")
def login(login:schemas.Login, db: Session = Depends(get_db_Ortak)):
    login = crud.giris(login=login, db=db)
    if(login==1):
        return {'Sonuc':'İşlem başarılı'}
    elif(login==2):
        return {'Sonuc':'Müsteri koduna ait lisans yok'}
    elif(login==3):
        return {'Sonuc':'Email veya şifre hatalı'}
    else:
        return  {'Sonuc':'Hay aksi'}

#Lisans List
@app.get("/lisanslar/")
def lisanslar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_Ortak)):
    lisanlar = crud.lisanslar(db, skip=skip, limit=limit)
    return lisanlar
