import os
from urllib.parse import urlparse

class BaseConfig:
    def __init__(self) -> None:
        # Server (Overriden when deployed)
        self.HOST: str = 'localhost'
        self.PORT: int = 5000
        self.IS_DEPLOYED: bool = False
        
        # PostgreSQL (Overriden when deployed)
        self.DB_NAME: str = 'postgres'
        self.DB_USER: str = 'postgres'
        self.DB_PASSWORD: str = '123'
        self.DB_HOST: str = None
        self.DB_PORT: int = None
        self.DB_SSL: str = None

        # Used by flask internally
        self.SECRET_KEY: str = 'zxcasdq12312gteshdkeasd123ASDzxcdhQWpt123a'
        self.SECURITY_PASSWORD_SALT = 'xogyj30gmjew9o39tjksxmpfkltn4vy9s'

        # Mail server
        self.MAIL_SERVER = 'smtp.googlemail.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_TLS = False
        self.MAIL_USE_SSL = True

        # Gmail login for sending account verification
        self.MAIL_USERNAME = 'transaticka.project@gmail.com'
        self.MAIL_PASSWORD = 'narrowpiano100'

class HerokuConfig(BaseConfig):
    def __init__(self) -> None:
        super().__init__()

        self.PORT = os.environ['PORT']
        self.IS_DEPLOYED = True

        db = urlparse(os.environ.get('DATABASE_URL'))
        self.DB_NAME = db.path[1:]
        self.DB_USER = db.username
        self.DB_PASSWORD = db.password
        self.DB_HOST = db.hostname
        self.DB_PORT = db.port
        self.DB_SSL = 'require'

def get_config() -> BaseConfig:
    if 'DYNO' in os.environ:
        return HerokuConfig()
    return BaseConfig()