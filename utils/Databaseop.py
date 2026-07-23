from models.database import db,User,Config,Login
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
import hashlib
from flask import current_app

def writedb(data,update=0):
    #first extract the nesscary
    username=data.get("username")
    password=data.get("password")
    if(not username or not password):
        return [0,"username or password not availabe"]
    email=data.get("email")
    password=__hashing(password)
    ROW=User(username=username,password=password,email=email)
    try:
        db.session.add(ROW)
        db.session.commit()
        
    except  IntegrityError:
        db.session.rollback()
        return [0,"The username  already exist"]
    except Exception as e:
        db.session.rollback()
        return [0,str(e)]
    return [1,ROW.userid]
        
        
     
    
def updatedb(data):
    result=readdb(data,input=1)
    if not result[0]:
        return [0,"No user found"]
    ROW=result[1]
    if not ROW:
        return[0,"NO user found"]
    
    email=data.get("email")
    if email:
        ROW.email=email
    pasword=data.get("password")
    if pasword:
        pasword=__hashing(pasword)
        ROW.password=pasword
    username=data.get("username")
    if username:
        ROW.username=username
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return [0, "Username or email already exists"]
    except Exception as e:
        db.session.rollback()
        return [0,str(e)]
    return [1,"Updated succefully"]
    

def saveapi(api,userid=None,username=None):
    try:
        ROW=db.session.query(User).filter(
            or_(User.username==username,User.userid==userid) ).first()
        if not ROW:
            return [0,"User is not found"]
    except Exception as e:
        return [0,str(e)]
    api=encription(text=api)
    ROW.api=api
    try:
        db.session.commit()
        return [1,"API saved successfully"]
    except Exception as e:
        db.session.rollback()
        return [0,str(e)]
    

    
def readdb(data,input=0):
    username=data.get("username")
    password=data.get("password")
    if(not password):
        return [0,"password not availabe"]
    email=data.get("email")
    
    try:
        ROW=db.session.query(User).filter(
            or_(User.username==username,User.email==email) ).first()
        if not ROW and not input:
            userid=data.get("userid")
            if not userid: #measn data is complelty wrong
                return [0,"No user found"]
            try: #also check by username also 
                ROW=db.session.query(User).filter_by(userid=userid).first()
            except Exception as e:
                return [0,str(e)]
        if not ROW:
            return[0,"No user found"]
        if input:
            return [1,ROW]
        ROWPASS=ROW.password
        USERID=ROW.userid
    
    except Exception as e:
        return [0,str(e)]
    
    password=__hashing(password)
    if ROWPASS==password:
           return [1,USERID]
    else:
        return [0,"username and password is incorrect"]
        

def readapi(api):
    api=encription(text=api) #decripting the data
    try:
        ROW=db.session.query(User).filter_by(api=api).first()
        if not ROW:
            return [0,"No api found"]
    except Exception as e:
        return [0,str(e)]
    return [1,ROW]

def writeconfig(data):
    userid=data.get("userid")
    allowusers=data.get("users")
    try:
        ROW=db.session.query(User).filter_by(userid=userid).first()
        if not ROW:
            return [0,"No api found"]
    except Exception as e:
        return [0,str(e)]
    CONFIGROW=ROW.Configs[0] if ROW.Configs else None
    if CONFIGROW is None:
        CONFIGROW=Config()
        ROW.Configs.append(CONFIGROW)
    CONFIGROW.url=data.get("link")
    CONFIGROW.allowusers=allowusers
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return [0,str(e)]
    return [1,CONFIGROW]

def getemail(email):
    try:
        ROW=db.session.query(User).filter_by(email=email).first()
        if not ROW:
            return [0,"No email found"]
        else:
            return [1,ROW.userid]
    except Exception as e:
        return [0,str(e)]
    
    
def changepwd(useid,password):
        ROW=db.session.query(User).filter_by(userid=useid).first()
        password=__hashing(password)
        try:
            ROW.password=password
            db.session.commit()
            return [1,"Password changed succefully"]
        except Exception as e:
                db.session.rollback()
                return [0,f"Thier has been a error {e}"]


def deletedb(data):
    result=readdb(data,input=1)
    if not result[0]:
        return [0,"No user found"]
    ROW=result[1]
    if not ROW:
        return[0,"No user found"]
    try:
        db.session.delete(ROW)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return [0,str(e)]
    return [1,"Delete succesdully"]


def writelogin(data):
    userid=data.get("userid")
    code=data.get("code")
    userpassword=__hashing(data.get("userpassword")) if data.get("userpassword") else None
    try:
        ROW=db.session.query(User).filter_by(userid=userid).first()
        if not ROW:
            return [0,"No api found"]
    except Exception as e:
        return [0,str(e)]
    LOGINROW=ROW.Logins[0] if ROW.Logins else None
    if LOGINROW is None:
        LOGINROW=Login()
        ROW.Logins.append(LOGINROW)
    LOGINROW.code=code
    LOGINROW.userpassword=userpassword
    try:
        db.session.commit()
        return [1,LOGINROW]
    except Exception as e:
        return [0,str(e)]
        

def readlogin(data):
    code=data.get("code")
    try:
        ROW=db.session.query(Login).filter_by(code=code).first()
        if not ROW:
            return [0,"No Link associated to the account found", None]
        else:
            return [1, ROW.userid, ROW.userpassword]
    except Exception as e:
        return [0,str(e), None]

def getlink(userid):
     from time import time
     ROW=db.session.query(Config).filter_by(userid=userid).first()
     if not ROW:
         return [0,"NO URL FOUND", False]
     currenttime=int(time())
     if ROW.valid<currenttime:
         return [0,"Time exceeded create a another link ",False]
     ROW.valid=currenttime+(24*7*60*60)
     try:
         db.session.commit()
     except Exception as e:
         db.session.rollback()
         #Can punish for my fault
     return [1, ROW.url, ROW.allowusers if ROW.allowusers is not None else True]
        
         

def __hashing(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encription(text: str, decrypt: bool = False) -> str:
    key = current_app.config["secret"]

    if isinstance(key, str):
        key = key.encode()

    if decrypt:
        data = bytes.fromhex(text)
    else:
        data = text.encode()

    result = bytes(
        b ^ key[i % len(key)]
        for i, b in enumerate(data)
    )

    return result.decode() if decrypt else result.hex()