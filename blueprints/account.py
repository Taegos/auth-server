from flask import Blueprint, request, Response, current_app, jsonify
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from account_model import Account
from token_gen import generate_token
from peewee import DoesNotExist
import bcrypt

account = Blueprint('account', __name__)

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
    except KeyError:
        return 'Request not formated correctly', 400
    
    if len(password) < 8:
        return "Password has to be atleast 8 characters long", 400
    if display_name == '':
        return "Display name cannot be empty", 400

    # Delete unconfirmed accounts with same email or display name
    Account.delete().where(
        Account.email == email or 
        Account.display_name == display_name and 
        Account.email_confirmed == False).execute()
    
    try:
        Account.create(
            email=email,
            password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            display_name=display_name,
        )
    except Exception as e:
        print(e)
        return str(e), 400

    if send_verification_email(email):
        return Response(status=201)
    return "Failed to send verification mail", 400

@account.route('login', methods=['POST'])
def login():
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
    
    return jsonify(generate_token(account.email, account.display_name, account.is_admin)), 201

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
    except Exception:
        return 'Request not formated correctly', 400
    
    try:
        account = Account.get(Account.email == email)
    except DoesNotExist:
        return 'Account with that email does not exist', 400
    
    if account.email_confirmed:
        return "Already confirmed", 400
    
    Account.update(email_confirmed=True).where(Account.email == email).execute()
    return 'Email confirmed, you can now login!', 201