from flask import Blueprint,jsonify,request
from utils.acceptjson import getjson
from utils.Databaseop import readlogin
from flask_jwt_extended import create_access_token, get_jwt_identity
from utils.Databaseop import getlink
Frontendreq=Blueprint("frontend",__name__)

##This is where yo uwill login hte frontend and then get the acces tooken

@Frontendreq.route("/login/url/",methods=["GET"])
@getjson
def home(data): #send userid or username 
    uniqueid=readlogin(data)
    if not uniqueid[0]:
        return jsonify({"return":uniqueid[1]}),401
    tooken=create_access_token(identity=uniqueid[1])
    return jsonify({"return":tooken,"userid":uniqueid[1]}),200
    



@Frontendreq.route("/url/",methods=["GET"])
@getjson
def index(data):
    code = request.headers.get("code")
    data["code"]=code
    output=readlogin(data) ##Here retive from memory but for now use db
    if not output[0]:
        return jsonify({"return":output[1]}),401
    userid = output[1]
    
    url_res = getlink(userid)
    if not url_res[0]:
        return jsonify({"return":url_res[1]}),404
    return jsonify({"url":url_res[1]}),200
    