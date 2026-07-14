from flask import Blueprint,jsonify
from utils.acceptjson import getjson
from utils.createapikey import APIKEY
from utils.Databaseop import writedb


accountcreationbp=Blueprint("createaccount",__name__)
@accountcreationbp.route("/createaccount/",methods=["POST"])
@getjson
def home(data):

    userid=writedb(data)
    if not userid[0]:
        return jsonify({"return":userid[1]}),401
    username=data.get("username")
    tooken=APIKEY(identity=username)
    
    return jsonify({"return":tooken,"userid":userid[1]}),200
    
