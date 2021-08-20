from flask import Flask
from blueprints.account import account
from blueprints.index import index
from account_model import Account
import os

app = Flask(__name__)

app.config.update(
    
    # main config
    SECRET_KEY = 'zxcasdq12312gteshdkea',
    SECURITY_PASSWORD_SALT = 'xogyj30gmjew9o39tjksxmpfkltn4vy9s',
    DEBUG = False,
    #BCRYPT_LOG_ROUNDS = 13
    #WTF_CSRF_ENABLED = True
    #DEBUG_TB_ENABLED = False
    #DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,

    # gmail authentication
    MAIL_USERNAME = 'project.shyft@gmail.com',
    MAIL_PASSWORD = 'wowsar132',

    # PostgreSQL
    POSTGRESQL_PASSWORD = '123'
)


app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(index, url_prefix='/')

if __name__ == '__main__':
    host = 'localhost'
    port = '5000'
    # When deployed to Heroku, host and port is provided as environment variables
    if 'HOST' in os.environ and 'PORT' in os.environ:
        host = os.environ['HOST']
        port = os.environ['PORT']
        
    app.run(host, port)