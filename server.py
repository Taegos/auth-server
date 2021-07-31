from flask import Flask
from account_model import Account
from db import db
from blueprints.account import account
from blueprints.auth import auth
from blueprints.index import index
import os

# Interesting stuff to consider
#https://git-secret.io/
#https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server
#https://stackoverflow.com/questions/9554087/setting-an-environment-variable-in-virtualenv

db.create_tables([Account])

app = Flask(__name__)

app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(index, url_prefix='/')

if __name__ == '__main__':

    host = '127.0.0.1'
    port = 5000
    
    # When deployed to Heroku, host and port is provided as environment variables
    if 'HOST' in os.environ and 'PORT' in os.environ:
        host = os.environ['HOST']
        port = os.environ['PORT']
        
    app.run(host, port)