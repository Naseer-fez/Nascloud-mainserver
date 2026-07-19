from flask import Blueprint,jsonify
from utils.acceptjson import getjson
from utils.createapikey import APIKEY
from utils.Databaseop import writedb, encription


accountcreationbp=Blueprint("createaccount",__name__)
@accountcreationbp.route("/register",methods=["POST"])
@accountcreationbp.route("/createaccount/",methods=["POST"])
@getjson
def home(data):

    userid=writedb(data)
    if not userid[0]:
        return jsonify({"return":userid[1]}),401
    uid = userid[1]
    username=data.get("username")
    tooken=APIKEY(username)
    
    from models.database import db, User, Login, Config
    user = db.session.query(User).filter_by(userid=uid).first()
    user.api = encription(tooken)
    
    import uuid
    code = str(uuid.uuid4().hex[:8])
    
    login_entry = Login(userid=uid, code=code)
    db.session.add(login_entry)
    
    config_entry = Config(userid=uid, url="", allowusers=True)
    db.session.add(config_entry)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"return": str(e)}), 500
        
    return jsonify({"api_key": tooken, "code": code, "server_url": "", "userid": uid}), 200
    
