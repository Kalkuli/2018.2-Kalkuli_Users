from project import db
from sqlalchemy_utils import PasswordType, EmailType, force_auto_coercion

force_auto_coercion()

class Company(db.Model):
    __tablename__ = 'company'
    id           = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    company_name = db.Column(db.String(128), nullable=False)
    cnpj         = db.Column(db.Integer,     nullable=False)
    users        = db.relationship('User',   backref='company', lazy=True)
    
    def __init__(self, company_name, cnpj):
        self.company_name = company_name
        self.cnpj         = cnpj


class User(db.Model):
    __tablename__ = 'user'
    id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    name       = db.Column(db.String(128), nullable=False)
    email      = db.Column(EmailType,      nullable=False)
    is_admin   = db.Column(db.Boolean(),   default=False, nullable=False)
    company_id = db.Column(db.Integer,     db.ForeignKey('company.id'), nullable=False)
    password   = db.Column(PasswordType(schemes=[ 'pbkdf2_sha512' ]), unique=False,nullable=False)
    
    def __init__(self, name, email, is_admin, company_id, password):
        self.name       = name
        self.email      = email
        self.is_admin   = is_admin
        self.company_id = company_id
        self.password   = password


 
        
    