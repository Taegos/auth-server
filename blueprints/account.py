from flask import Blueprint, request, current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message, Mail
from peewee import DoesNotExist, IntegrityError
import bcrypt

from models.account import Account

account = Blueprint('account', __name__)

def send_verification_email(email):
    token = URLSafeTimedSerializer(current_app.config['SECRET_KEY']).dumps(
        email, 
        salt=current_app.config['SECURITY_PASSWORD_SALT']
    )
    # See confirm_mail route at the bottom of file
    confirm_link = f"{request.host_url}account/confirm_mail/{token}"
    msg = Message("Welcome to Transaticka!",
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[email],
                  html = current_app.config['MAIL_VERIFICATION_HTML'].format(confirm_link))
    mail = Mail(current_app)
    try:
        
        mail.send(msg)
        return True
    except Exception:
        return False
   
@account.route('', methods=['POST'])
def post():
    try:
        email = request.json['email']
        password = request.json['password']
        display_name = request.json['display_name']
    except KeyError:
        return 'Request not formated correctly', 400
    
    if len(password) < 8:
        return "Password has to be atleast 8 characters long", 400
    if len(display_name) < 4:
        return "Display name has to be atleast 4 characters long", 400

    if not send_verification_email(email):
        return "Failed to send verification mail", 400

    try:
        Account.create(
            email=email,
            display_name=display_name,
            password_hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )
    except IntegrityError as e:
        return "Email or display name already exists", 409

    return f"Registration succeeded, a verification mail was sent to '{email}'", 201

@account.route('confirm_mail/<token>', methods=['GET'])
def confirm_mail(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=3600
        )
    except Exception:
        return 'Invalid confirmation link', 400
    
    try:
        account = Account.get(Account.email == email)
    except DoesNotExist:
        return 'Account with that email does not exist', 400
    
    if account.email_confirmed:
        return "Already confirmed", 400
    
    Account.update(email_confirmed=True).where(Account.email == email).execute()
    return 'Email confirmed, you can now login!', 200 