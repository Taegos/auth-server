from flask import Flask

from models.database import get_database, init_database
from config import LocalConfig, HerokuConfig

def _setup_db(): 
    from models.account import Account
    from peewee import IntegrityError
    from bootstrapper.create_accounts import create_example_accounts

    try:
      #  if not is_deployed_to_heroku():
        get_database().drop_tables([Account])
        get_database().create_tables([Account])
        create_example_accounts()
    except Exception as e:
        print("EXCEPTION " + str(e))

def create_app(config: object):
    init_database(config) # Needs to come before anything else

    _setup_db()

    from blueprints.account import account
    from blueprints.auth_token import auth_token
    from blueprints.index import index

    app = Flask(__name__)
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(auth_token, url_prefix='/auth_token')
    app.register_blueprint(index, url_prefix='/')
    
    app.config.from_object(config)
    return app

def create_heroku_app():
    return create_app(HerokuConfig())
    
if __name__ == '__main__':
    app = create_app(LocalConfig())
    app.run()