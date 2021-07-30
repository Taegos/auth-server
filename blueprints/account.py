from flask import Blueprint, request, jsonify
from account_model import Account
from token_gen import generate_token
import bcrypt

account = Blueprint('account', __name__)

@account.route('', methods=['POST'])
def post():
    try:
        email = request.json['email']
        password = request.json['password']
    except KeyError as e:
        return 'Request not formated correctly', 400
        
    query = Account.select().where(Account.email == email)
    if query.exists():
        return f"A user with email '{email}' already exists", 400
    if len(password) < 8:
        return "Password has to be atleast 8 characters long", 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    id = Account.create(email=email, password_hash=password_hash)
    return jsonify(generate_token(id)), 201
