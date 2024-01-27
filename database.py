from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Email(db.Model):
    
    __tableanme__ = 'emails'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=True)
    service = db.Column(db.String(50), nullable=False)

class Password(db.Model):
    
    __tableanme__ = 'passwords'
    
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

def connect_db(app):
    db.app = app
    db.init_app(app)

