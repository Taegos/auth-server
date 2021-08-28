from peewee import IntegrityError
from flask import Flask, config
import os
import db
from bootstrapper.create_example import create_example_account
from config import LiveConfig, LocalConfig
from blueprints.index import index
from blueprints.account import account
from blueprints.auth_token import auth_token

def create_app():
    app = Flask(__name__)
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(account, url_prefix='/account')
    app.register_blueprint(auth_token, url_prefix='/auth_token')
    return app

def create_live_app():
    if os.environ.get("LIVE") is None:
        raise Exception("Cannot run live app, LIVE environment variable is not set")
    config: LiveConfig = LiveConfig()
    db.connect(config)
    #db.reset()
   # try:
   #     for display_name in config.EXAMPLE_ACCOUNTS:
   #        create_example_account(display_name)
   # except IntegrityError:
    #    pass
    app = create_app()
    app.config.from_object(config)
    return app

def create_local_app(config: LocalConfig):
    if os.environ.get("LIVE") is not None:
        raise Exception("Cannot run testing app, LIVE environment variable is set")
    db.connect(config)
    db.reset
    app = create_app()
    app.config.from_object(config)
    return app

if __name__ == '__main__':
    app = create_local_app(LocalConfig())
    app.run()