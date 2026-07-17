from flask  import Flask
import os
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models.database import db
from routes.health import healthbp
from routes.Useroperations.Login import loginbp
from routes.Useroperations.creatacc import accountcreationbp
from routes.Useroperations.deleteacc import deleteacc
from routes.Useroperations.update import updatebp
from routes.Useroperations.Forgotemail.forgotemail import forgotbp
from routes.reqfrmserv import reqfrmbac
from routes.Frontendreq import Frontendreq
from routes.dashboard import dashbaord
from utils.auth import enableauth
from utils.ratelimiter import enableratelimiter
from utils.logs import logs
from datetime import timedelta
load_dotenv()
def createapp():
    app=Flask(__name__)
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        allow_headers=["*"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        supports_credentials=False,
    )
    app.config["secret"]=os.getenv("secret")
    app.config["JWT_SECRET_KEY"]=os.getenv("jwt") or os.getenv("secret")
    routes=[healthbp,loginbp,accountcreationbp,deleteacc,updatebp,forgotbp,
            reqfrmbac,Frontendreq,dashbaord]
    for endpoint in routes:
        app.register_blueprint(endpoint)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(int(os.getenv("jwtduration",30)))
        #DATABASE
    database_url = os.getenv("Database", "sqlite:///users.db")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   
    JWTManager(app)
    enableratelimiter(app)
    enableauth(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    logs(app)
        
    return app

app=createapp()
if __name__=="__main__":
    app.run(debug=True)