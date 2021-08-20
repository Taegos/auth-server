from flask import Blueprint, request, Response, session, current_app, jsonify
from token_gen import generate_token
from itsdangerous import URLSafeTimedSerializer
from functools import wraps
from flask_mail import Message, Mail
import time
import bcrypt

from db import db

account = Blueprint('account', __name__)
#db.accounts.drop()

def send_verification_email(email):
    token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(
        email, 
        salt=current_app.config['SECURITY_PASSWORD_SALT']
    )
    msg = Message("Welcome to Transaticka!",
                  sender="transaticka@gmail.com",
                  recipients=[email],
                  html = f"Click to verify your email: {request.host_url}account/confirm_mail/{token}")
    mail = Mail(current_app)
    try:
        mail.send(msg)
        return True
    except:
        return False

@account.route('register', methods=['POST'])
def register():
    try:
        email = request.json['email']
        password = request.json['password']
        display_name = request.json['display_name']
    except KeyError as e:
        return 'Request not formated correctly', 400
    
    if len(password) < 8:
        return "Password has to be atleast 8 characters long", 400
    if display_name == '':
        return "Display name cannot be empty", 400

    # If account with email or display name is found but is not confirmed yet, overwrite
    existing = db.accounts.find_one({'email': email })
    if existing is not None:
        if not existing['email_confirmed']:
            db.accounts.delete_one({'email': email })
        else:
            return "That email is already in use", 400
    
    existing = db.accounts.find_one({'display_name': display_name })
    if existing is not None:
        if not existing['email_confirmed']:
            db.accounts.delete_one({'display_name': display_name })
        else:
            return "That display name is already in use", 400

    db.accounts.insert_one({
        'email': email,
        'password_hash': bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        'display_name': display_name,
        'is_admin': False,
        'email_confirmed': False,
        'registered_at': (int)(time.time()),
    })

    if send_verification_email(email):
        return Response(status=201)
    return "Failed to send verification mail", 400

@account.route('login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']
    except KeyError as e:
        return 'Request not formated correctly', 400
    
    account = db.accounts.find_one({"email": email})
    if account is None:
        return "Invalid email or password", 401
    if not account["email_confirmed"]:
        return "Account not confirmed yet", 400
    password_hash = account['password_hash'].encode('utf-8')
    if bcrypt.hashpw(password.encode('utf-8'), password_hash) != password_hash:
        return "Invalid email or password", 401
    
    return jsonify(generate_token(account['email'], account['display_name'], account['is_admin'])), 201

def get_email_from_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.loads(
        token,
        salt=current_app.config['SECURITY_PASSWORD_SALT'],
        max_age=3600
    )

@account.route('confirm_mail/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = get_email_from_token(token)
    except Exception as e:
        return 'Request not formated correctly', 400
    
    account = db.accounts.find_one({"email": email})
    if account is None:
        return 'Account with that email does not exist', 400
    if account['email_confirmed']:
        return "Already confirmed", 400
    
    db.accounts.update_one({"email": email}, { "$set": { "email_confirmed": True } })
    return 'Email confirmed, you can now login!', 201