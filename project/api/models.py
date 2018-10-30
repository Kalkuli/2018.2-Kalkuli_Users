from project import db
from sqlalchemy_utils import PasswordType, EmailType

class Company(db.Model):
    __tablename__ = 'company'
    id            = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    company_name  = db.Column(db.String(128), nullable=False)
    cnpj          = db.Column(db.String,     nullable=True)
    users         = db.relationship('User',   backref='company', lazy=True)
    company_email = db.Column(db.String(128), nullable=False)
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
    id         = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    name       = db.Column(db.String(128), nullable=False)
    email      = db.Column(EmailType,      nullable=False)
    company_id = db.Column(db.Integer,     db.ForeignKey('company.id'), nullable=False)
    password   = db.Column(PasswordType(schemes=[ 'pbkdf2_sha512' ]), unique=False,nullable=False)
    
    def __init__(self, name, email, company_id, password):
        self.name       = name
        self.email      = email
        self.company_id = company_id
        self.password   = password
    