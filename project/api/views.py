from flask import request, jsonify, Blueprint
from sqlalchemy import exc, or_ 
from project.api.models import Company
from project.api.models import User
from project import db, bcrypt
from project.api.utils import authenticate
import time

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users', methods=['GET'])
def get_all_users():
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200

@user_blueprint.route('/user', methods=['POST'])
def add_company_user():
    post_data = request.get_json()

    error_response = {
        'status': 'fail',
        'message': 'company could not be saved'
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

    admin = post_data.get('user')
    
    username   = admin.get('username')
    email      = admin.get('email')
    password   = admin.get('password')

    try:
        company = Company(company_name, cnpj, company_email, fantasy_name, cep, city, state, company_phone)
        db.session.add(company)
        db.session.flush()

        admin = User.query.filter_by(email=email).first()
        if not admin:
            db.session.add(User(username=username, email=email, password=password, company_id=company.id))
            db.session.commit()
            response = {
                'status': 'success',
                'message': 'Company and user were created!'
            }
            return jsonify(response), 201
        else:
            response['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify({
            'status': 'fail',
            'message': 'company could not be saved'
        }), 400

@user_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    company_name  = post_data.get('company_name')
    cnpj          = post_data.get('cnpj')
    company_email = post_data.get('company_email')
    fantasy_name  = post_data.get('fantasy_name')
    cep           = post_data.get('cep')
    city          = post_data.get('city')
    state         = post_data.get('state')
    company_phone = post_data.get('company_phone')
    
    username   = post_data.get('username')
    email      = post_data.get('email')
    password   = post_data.get('password')
    try:
        company = Company(company_name, cnpj, company_email, fantasy_name, cep, city, state, company_phone)
        db.session.add(company)
        db.session.flush()  
        user = User.query.filter(
        or_(User.username == username, User.email == email)).first()
        if not user:
            new_user = User(
                username=username,
                email=email,
                password=password,
                company_id=company.id
            )       
            db.session.add(new_user)
            db.session.commit()
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully registered.'
            response_object['auth_token'] = auth_token.decode()
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That user already exists.'
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        return jsonify(response_object), 400

@user_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object['status'] = 'success'
                response_object['message'] = 'Successfully logged in.'
                response_object['auth_token'] = auth_token.decode()
                return jsonify(response_object), 200
            else:
                response_object['message'] = 'User does not exist.'
                return jsonify(response_object), 404
    except Exception as e:
        response_object['message'] = 'Try again.'
        return jsonify(response_object), 500

@user_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(resp):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200

@user_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(resp):
    user = User.query.filter_by(id=resp).first()
    response_object = {
        'status': 'success',
        'message': 'success',
        'data': user.to_json()
    }
    return jsonify(response_object), 200