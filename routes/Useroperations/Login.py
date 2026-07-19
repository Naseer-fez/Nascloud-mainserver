from flask import Blueprint,jsonify
from utils.acceptjson import getjson
from utils.createapikey import APIKEY
from utils.Databaseop import readdb,saveapi, encription
from models.database import db, User, Login, Config
loginbp=Blueprint("login",__name__)

@loginbp.route("/login/",methods=["POST"])
@getjson
def home(data):
    uniqueid=readdb(data)
    if not uniqueid[0]:
        return jsonify({"return":uniqueid[1]}),401
    userid = uniqueid[1]
    
    
    user = db.session.query(User).filter_by(userid=userid).first()
    
    api_key = user.api if user.api else ""
    if not api_key:
        api_key = APIKEY()
        user.api = encription(api_key)
    else:
        api_key = encription(api_key, decrypt=True)
        
    login_entry = user.Logins[0] if user.Logins else None
    if not login_entry:
        import uuid
        code = str(uuid.uuid4().hex[:8])
        login_entry = Login(userid=userid, code=code)
        db.session.add(login_entry)
    else:
        code = login_entry.code
        
    config_entry = user.Configs[0] if user.Configs else None
    if not config_entry:
        config_entry = Config(userid=userid, url="", allowusers=True)
        db.session.add(config_entry)
    server_url = config_entry.url if config_entry.url else ""
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"return": str(e)}), 500
        
    return jsonify({"api_key": api_key, "code": code, "server_url": server_url, "userid": userid}), 200
    
