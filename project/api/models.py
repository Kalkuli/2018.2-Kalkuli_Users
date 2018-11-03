from project import db
import datetime
import jwt
from project import create_app
from sqlalchemy_utils import PasswordType, EmailType
from project import bcrypt 
from flask import current_app


class Company(db.Model):
    __tablename__ = 'company'
    id            = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    company_name  = db.Column(db.String(128), nullable=False)
    cnpj          = db.Column(db.String,     nullable=True)
    users         = db.relationship('User',   backref='company', lazy=True)
    company_email = db.Column(db.String(128), nullable=False, unique=True)
    fantasy_name  = db.Column(db.String(128), nullable=True) 
    cep           = db.Column(db.String(128), nullable=True)
    city          = db.Column(db.String(128), nullable=True)
    state         = db.Column(db.String(128), nullable=True)
    company_phone = db.Column(db.String(128), nullable=True)
    
    def __init__(self, company_name, cnpj, company_email, fantasy_name, cep, city, state, company_phone):
        self.company_name  = company_name
        self.cnpj          = cnpj
        self.company_email = company_email
        self.fantasy_name  = fantasy_name
        self.cep           = cep
        self.city          = city
        self.state         = state
        self.company_phone = company_phone


class User(db.Model):
    __tablename__ = 'user'

    id            = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    username      = db.Column(db.String(128), nullable=False)
    email         = db.Column(EmailType,      nullable=False, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    company_id    = db.Column(db.Integer,     db.ForeignKey('company.id'), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    password      = db.Column(db.String(255), unique=False,nullable=False)
    
    def __init__(self, username, email, company_id, password):
        self.username      = username
        self.email         = email
        self.company_id    = company_id
        self.password      = bcrypt.generate_password_hash(password, current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        self.registered_on = datetime.datetime.now()

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e