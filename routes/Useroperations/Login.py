from flask import Blueprint,jsonify
from utils.acceptjson import getjson
from utils.createapikey import APIKEY
from utils.Databaseop import readdb,saveapi

loginbp=Blueprint("login",__name__)

@loginbp.route("/login/",methods=["POST"])
@getjson
def home(data):
    uniqueid=readdb(data)
    if not uniqueid[0]:
        return jsonify({"return":uniqueid[1]}),401
    return jsonify({"return":"Go to the dashboard for you api key","userid":uniqueid[1]}),200
    
