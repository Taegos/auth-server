from flask import Blueprint, request, jsonify
from account_model import Account
from peewee import DoesNotExist
from token_gen import generate_token
import bcrypt

auth = Blueprint('auth', __name__)

@auth.route('', methods=['POST'])
def post():

    try:
        email = request.json['email']
        password = request.json['password']
    except KeyError as e:
        return 'Request not formated correctly', 400

    try:
        account = Account.get(Account.email == email)
    except DoesNotExist as e:
        return "Invalid email or password", 401

    password_hash = account.password_hash.encode('utf-8')
    if bcrypt.hashpw(password.encode('utf-8'), password_hash) != password_hash:
        return "Invalid email or password", 401
    
    return jsonify(generate_token(account.id)), 201