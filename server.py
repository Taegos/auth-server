from flask import Flask
from account_model import Account
from db import db
from blueprints.account import account
from blueprints.auth import auth
from blueprints.index import index
from config import Config

#https://git-secret.io/
#https://stackoverflow.com/questions/29458548/can-you-add-https-functionality-to-a-python-flask-web-server

db.create_tables([Account])

app = Flask(__name__)

app.register_blueprint(account, url_prefix='/account')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(index, url_prefix='/')

app.run(Config.HOST, Config.PORT)