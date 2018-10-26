from flask import request, jsonify, Blueprint

from sqlalchemy import exc 
from project.api.models import Company
from project.api.models import User

from project import db

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/add_company', methods=['POST'])
def add_company():
    post_data = request.get_json()

    error_response = {
        'status': 'fail',
        'message': 'wrong json'
    }

    if not post_data:
        return jsonify(error_response), 400

    company = post_data.get('company')

    company_name  = company.get('company_name')
    cnpj          = company.get('cnpj')
    company_email = company.get('company_email')
    fantasy_name  = company.get('fantasy_name')
    cep           = company.get('cep')
    city          = company.get('city')
    state         = company.get('state')
    company_phone = company.get('company_phone')

    # admin = post_data.get('user')
    
    # name       = admin.get('name')
    # email      = admin.get('email')
    # is_admin   = None
    # company_id = admin.get('company_id')
    # password   = admin.get('password')

    try:
        company = Company(company_name, cnpj, company_email, fantasy_name, cep, city, state, company_phone)
        db.session.add(company)
        db.session.flush()

        # admin = User(name, email, is_admin, company.id, password)
        # db.session.add(admin)

        db.session.commit()

        response = {
            'status': 'success',
            'message': 'Company was created!'
        }

        return jsonify(response), 201
        
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify({
            'error': 'eerrro bizarro'
        }), 400