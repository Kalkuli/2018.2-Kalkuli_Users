from project import db
from project.api.models import User, Company

def add_user(username, email, password, company_id):
    user = User(username=username, email=email, password=password, company_id=company_id)
    db.session.add(user)
    db.session.commit()
    return user

def add_company(company_name, cnpj, company_email, fantasy_name, cep, city, state, company_phone):
    company = Company(company_name=company_name, cnpj=cnpj, company_email=company_email, fantasy_name=fantasy_name, cep=cep, city=city, state=state, company_phone=company_phone)
    db.session.add(company)
    db.session.commit()
    return company