from sqlalchemy.orm import Session

from . import models, schemas
import psycopg2

from psycopg2 import connect
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import random
import string

def drop_database(dbname:str):
    try:
        sonuc=1
        con = None
        con = connect(dbname='dbname', user='user', host='host', password='password')

        dbname = dbname

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('DROP DATABASE ' + dbname)
        cur.close()
        con.close()
    except Exception as e:
        sonuc=0
        print("hata  ")
        print(e)
    return sonuc

def get_random_string(length:int):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def auto_db(dbname:str):
    try:

        con = None
        con = connect(dbname='dbname', user='user', host='host', password='password')

        dbname = dbname

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE ' + dbname)
        cur.close()
        con.close()
    except Exception as e:
        print("hata  ")
        print(e)

def auto_table_user(dbname:str, tablename:str, user:schemas.UserCreate):
    try:
        arr=[]
        data=[]
        con = None
        con = connect(dbname=dbname, user='user', host='host', password='password')
        cur = con.cursor()

        sqlCreateTable = 'CREATE TABLE "'+tablename+'" (id serial NOT NULL, "name" varchar NULL, email varchar NULL, "password" varchar NULL);'
        cur.execute(sqlCreateTable)
        con.commit()

        arr=[user.name,user.email,user.password]
        data.append(arr)
        sql_insert="INSERT INTO "+ tablename+"(name,email,password) VALUES(%s,%s,%s)"
        number_of_rows=cur.executemany(sql_insert,data)
        con.commit()

        sql_select="SELECT name,email,password from"+tablename
        cur.execute(sql_select)
        records = cur.fetchall()
        name=""
        email=""
        password=""
        for row in records:
            name=row[0]
            email=row[1]
            password=row[2]
            print('name:'+str(name)+' email:'+str(email)+' password:'+str(password))
        con.close()
    except Exception as e:
        print("hata  ")
        print(e)

def kayit(user:schemas.UserCreate):
    sonuc=1
    name=""
    email=""
    password=""
    arr=[]
    data=[]
    arrLisans=[]
    dataLisans=[]
    
    try:
        con = None
        con = connect(dbname='dbname', user='user', host='host', password='password')

        dbname = "user_"+user.email

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        #Database Oluşturuluyor
        cur.execute('CREATE DATABASE ' + dbname)
        cur.close()
        con.close()
        print("Database oluşturuldu. Db name:"+dbname)

        #Tablo Oluşturuluyor
        tablename="users"
        con_User = None
        con_User = connect(dbname=dbname, user='user', host='host', password='password')
        cur_User = con_User.cursor()

        sqlCreateTable = 'CREATE TABLE "'+tablename+'" (id serial NOT NULL, "name" varchar NULL, email varchar NULL, "password" varchar NULL);'
        cur_User.execute(sqlCreateTable)
        con_User.commit()

        arr=[user.name,user.email,user.password]
        data.append(arr)
        sql_insert='INSERT INTO '+ tablename+'("name",email,"password") VALUES(%s,%s,%s)'
        number_of_rows=cur_User.executemany(sql_insert,data)
        con_User.commit()

        sql_select='SELECT "name",email,"password" from '+tablename
        cur_User.execute(sql_select)
        records = cur_User.fetchall()
        for row in records:
            name=row[0]
            email=row[1]
            password=row[2]
            print('Tablo oluşturuldu table name:'+tablename+' Data: name:'+str(name)+' email:'+str(email)+' password:'+str(password))
        con_User.close()
        #Eğer User tablosu oluşturulduysa Ortak(bendeki ismi deneme123) veritabanıda Lisanslar tablosuna Kayıt gerçekleşiyor.
        if(name!=""):

            musterikodu=get_random_string(length=6)
            dbusername='rotaboo'
            dbpassword='72021112*k'

            con_Lisans = None
            con_Lisans = connect(dbname='dbname_Ortak', user='user', host='host', password='password')
            cur_Lisans = con_Lisans.cursor()
            
            arrLisans=[str(musterikodu),dbname,dbusername,dbpassword]
            dataLisans.append(arrLisans)
            sql_insert_lisans="INSERT INTO lisanslar (musterikodu,dbname,dbusername,dbpassword) VALUES(%s,%s,%s,%s)"
            number_of_rows_Lisans=cur_Lisans.executemany(sql_insert_lisans,dataLisans)
            con_Lisans.commit()

            sql_select_Lisans="SELECT musterikodu,dbname,dbusername,dbpassword from lisanslar Where musterikodu='"+musterikodu+"'"
            cur_Lisans.execute(sql_select_Lisans)
            records_Lisans = cur_Lisans.fetchall()
            musterikodu=""
            dbname=""
            dbusername=""
            dbpassword=""
            for row in records_Lisans:
                musterikodu=row[0]
                dbname=row[1]
                dbusername=row[2]
                dbpassword=row[2]
                print('Lisans tablosuna kayıt gerçekleşti Data: musterikodu:'+str(musterikodu)+' dbname:'+str(dbname)+' dbusername:'+str(dbusername)+' dbpassword:'+str(dbpassword))
            con_Lisans.close()
    except Exception as e:
        sonuc=0
        print("hata  ")
        print(e)
    return sonuc

def lisanslar(db:Session, skip: int = 0, limit: int = 100):
    return db.query(models.Lisanslar).offset(skip).limit(limit).all()

def giris(login:schemas.Login, db: Session):
    try:
        sonuc=1
        dbname=""
        dbusername =""
        dbpassword =""
        email=""
        password=""

        ortak_lisans=db.query(models.Lisanslar).filter(models.Lisanslar.musterikodu == login.musterikodu).first()
        if(ortak_lisans):
            dbname=ortak_lisans.dbname
            dbusername=ortak_lisans.dbusername
            dbpassword=ortak_lisans.dbpassword
        else:
            sonuc=2 #Müsteri koduna ait lisans yok
        if(sonuc==1):
            con_User = None
            con_User = connect(dbname=dbname, user=dbusername, host='host', password=dbpassword)
            cur_User = con_User.cursor()

            sql_select='SELECT email,"password" from users'
            cur_User.execute(sql_select)
            records = cur_User.fetchall()
            for row in records:
                email=row[0]
                password=row[1]
            con_User.close()
            if(email==login.email and password==login.password):
                sonuc=1 #Giriş başarılı
            else:
                sonuc=3 #Email veya şifre hatalı
    except Exception as e:
        sonuc=0 #Kod hatalı
        print("hata  ")
        print(e)
    return sonuc