from flask import Flask

from models.database import get_database, connect_database
from config import BaseConfig, HerokuConfig

def _populate_database(config: BaseConfig): 
    from models.account import Account
    from peewee import IntegrityError
    from bootstrapper.create_accounts import create_accounts

    try:
        if not config.IS_DEPLOYED:
            get_database().drop_tables([Account])
        get_database().create_tables([Account])
        create_accounts(
            'Ghaf',
            'Brind',
            'Alchemight',
            'Incantates',
            'Dreadfuls',
            'Burvalr',
            'Khurkmostroll'
        )
    except Exception as e:
        pass
    
    get_database().create_tables([Account])
    

def create_app(config: object):
    connect_database(config) # Needs to come before anything else

    _populate_database(config)

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
    app = create_app(BaseConfig())
    app.run()