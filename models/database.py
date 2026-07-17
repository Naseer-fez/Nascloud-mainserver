from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class User(db.Model):
    __tablename__="User"
    userid=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(256),nullable=False,unique=True)
    password=db.Column(db.String(256),nullable=False)
    email=db.Column(db.String(256),nullable=True,unique=True)  
    api=db.Column(db.String(512),nullable=True,unique=True)
    Configs = db.relationship(
        "Config",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )
    Logins=db.relationship(
        "Login",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan"
    )

class Login(db.Model):
    __tablename__="Login"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    userid = db.Column(
    db.Integer,
    db.ForeignKey("User.userid", ondelete="CASCADE"),
    index=True,
    nullable=False
        )
    code=db.Column(db.String(10))
    userpassword=db.Column(db.String(256),nullable=True)
    
    
class Config(db.Model):
    __tablename__="Config"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    userid = db.Column(
        db.Integer,
        db.ForeignKey("User.userid", ondelete="SET NULL"),
        index=True,
        nullable=True
    )
    url=db.Column(db.String(768),nullable=True)
    allowusers=db.Column(db.Boolean,nullable=True,default=True) ##measn allow users