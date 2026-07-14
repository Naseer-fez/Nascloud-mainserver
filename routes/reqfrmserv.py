from flask import Blueprint,jsonify
from utils.acceptjson import getjson
from utils.Databaseop import readapi,writeconfig,writelogin
reqfrmbac=Blueprint("backend",__name__)

@reqfrmbac.route("/register/api/",methods=["GET"])
@getjson
def home(data):
    API=data.get("api")
    output=readapi(API)
    if not  output[0]:
        return jsonify({"return":output[1]}),401
    ROW=output[1]
    #That measn the api is registred 
    ngroklink=data.get("link")
    if not ngroklink:
        return jsonify({"return":"No link provided"}),401
    allowusers=int(data.get("users"))
    data["userid"]=ROW.userid
    savethedata=writeconfig(data)
    if not  savethedata[0]:
        return jsonify({"return":savethedata[1]}),401
    return jsonify({"return": "success"}), 200
    
    
@reqfrmbac.route("/register/user/",methods=["POST"])
@getjson
def index(data):
    API=data.get("api")
    output=readapi(API)
    if not  output[0]:
        return jsonify({"return":output[1]}),401
    ROW=output[1] #Now i need to take this 
    data["userid"]=ROW.userid
    output=writelogin(data)
    ##Here save in in memory
    if not  output[0]:
        return jsonify({"return":output[1]}),401
    return jsonify({"message":f"""{data.get("code")} is the code registred
                    The password is {data.get("userpassword")}
            Use this credentials to login.
                    """ })
    
