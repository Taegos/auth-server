from flask import Flask

from config import get_config
from models.database import get_database, init_database
from util.is_deployed_to_heroku import is_deployed_to_heroku

def _create_tables(): 
    from models.account import Account
    from peewee import IntegrityError
    try:
      #  if not is_deployed_to_heroku():
        get_database().drop_tables([Account])
        get_database().create_tables([Account])
    except IntegrityError as e:
        print(e)

def create_app(config: object):
    init_database(config) # Needs to come before anything else

    _create_tables()
    from bootstrapper.create_accounts import create_example_accounts
    create_example_accounts()

    from blueprints.account import account
    from blueprints.auth_token import auth_token
    from blueprints.index import index

    app = Flask(__name__)
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(auth_token, url_prefix='/auth_token')
    app.register_blueprint(index, url_prefix='/')
    
    app.config.from_object(config)
    app.run(config.HOST, config.PORT)
    return app