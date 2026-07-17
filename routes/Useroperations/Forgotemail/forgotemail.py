from flask import Blueprint,jsonify,request
from utils.acceptjson import getjson
from .codegen import OTP
from .memdb import STORAGE
forgotbp=Blueprint("forgot",__name__)

@forgotbp.route("/forgot",methods=["POST"])
@forgotbp.route("/forgot/",methods=["POST"])
@getjson
def home(data):
    email=data.get("email")
    if not email:
        return jsonify({"return":"no email sent"}),400
    
    from utils.Databaseop import getemail
    code_res = getemail(email)
    if not code_res[0]:
        return jsonify({"return": "No account found with this email"}), 404
        
    userid = code_res[1]
    from models.database import db, User
    user = db.session.query(User).filter_by(userid=userid).first()
    login_entry = user.Logins[0] if user.Logins else None
    if not login_entry or not login_entry.code:
        return jsonify({"return": "No unique identifier associated with this account"}), 404
        
    from utils.sendemail import Messages_to_send
    Subject = "Your PersonalDrive Unique Identifier Recovery"
    Content = f"""
    Hello,
    
    You requested to recover your unique identifier for PersonalDrive.
    
    Your Unique Identifier (Code) is: {login_entry.code}
    
    You can use this identifier to resolve your server and log in.
    
    Thank you!
    """
    statement = Messages_to_send(to=email, subject=Subject, content=Content)
    if not statement[0]:
        return jsonify({"return": f"Failed to send email: {statement[1]}"}), 500
        
    return jsonify({"return": "Recovery email sent successfully"}), 200





@forgotbp.route("/forgot/code/",methods=["POST"])
@getjson
def code(data):
    code=request.headers.get("otp")
    if not code:
        return jsonify({"return":"no otp sent"}),401
    email=data.get("email")
    if not email:
        return jsonify({"return":"no email sent"}),401
    info=STORAGE(email=email,otp=code,action="check")
    if not (info[0]):
            return jsonify(info[1]),401
    return jsonify(info[1]),200
    
    
@forgotbp.route("/verify/code/",methods=["POST"])
@getjson
def verify(data):
    code=request.headers.get("token")
    if not code:
        return jsonify({"return":"no otp sent"}),401
    password=data.get("password")
    email=data.get("email")
    value=STORAGE(email=email,password=password,tooken=code,action="token")
    if not value[0]:
        return jsonify(value[1]),401
    return jsonify({"return":"Password changed"}),200
    
    

    