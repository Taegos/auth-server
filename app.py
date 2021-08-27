from peewee import IntegrityError
from flask import Flask, config

import db
from bootstrapper.create_example import create_example_account
from config import BaseConfig, HerokuConfig
from blueprints.index import index
from blueprints.account import account
from blueprints.auth_token import auth_token
from models.account import proxy

def create_app(config: BaseConfig):
    db.connect(config)
    
    try:
        for display_name in config.EXAMPLE_ACCOUNTS:
           create_example_account(display_name)
    except IntegrityError:
        pass

    app = Flask(__name__)
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(auth_token, url_prefix='/auth_token')
    app.config.from_object(config)
    
    return app

def create_heroku_app():
    return create_app(HerokuConfig())

if __name__ == '__main__':
    app = create_app(BaseConfig())
    app.run(config.HOST, config.PORT)