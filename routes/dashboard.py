from flask import Blueprint
from flask import Blueprint,jsonify
from utils.acceptjson import getjson
from utils.createapikey import APIKEY
from utils.Databaseop import readdb,saveapi

dashbaord=Blueprint("dashboard",__name__)
#this  return the api key which helps in configuring the centralserver
@dashbaord.route("/dashboard/",methods=["POST"])
@getjson
def home(data):
    userdetail=readdb(data,input=1) ##measn first verfiy the credentails username and password
    if not userdetail[0]:
        return jsonify({"return":"wrong credentials"}),401
    ROW=userdetail[1]
    tooken=APIKEY(uid=ROW.userid)
    save= saveapi(userid=ROW.userid,username=ROW.username,api=tooken)
    if not save[0]:
        return jsonify({"return":save[1]}),401
    return jsonify({"return":tooken}),200
    
    


