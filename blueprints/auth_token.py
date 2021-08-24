from flask import Blueprint, request, jsonify
from peewee import DoesNotExist
import bcrypt

import util.rsa
from models.account import Account

auth_token = Blueprint('auth_token', __name__)

@auth_token.route('', methods=['GET'])
def get():
    try:
        email = request.json['email']
        password = request.json['password']
    except KeyError:
        return 'Request not formated correctly', 400

    try:
        account = Account.get(Account.email == email)
        if not account.email_confirmed:
            return "Account not confirmed yet", 400
        password_hash = account.password_hash.encode('utf-8')
        if bcrypt.hashpw(password.encode('utf-8'), password_hash) != password_hash:
            return "Invalid email or password", 401
    except DoesNotExist:
        return "Invalid email or password", 401
    
    payload = {
        'uuid': account.uuid,
        'display_name': account.display_name,
        'is_admin': account.is_admin
    }
    token = util.rsa.sign_payload(payload)
    return jsonify(token), 200