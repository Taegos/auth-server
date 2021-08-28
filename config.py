import os
from urllib.parse import urlparse

class LiveConfig:
    def __init__(self) -> None:

        # PostgreSQL
        db = urlparse(os.environ.get('DATABASE_URL'))
        self.DB_NAME = db.path[1:]
        self.DB_USER = db.username
        self.DB_PASSWORD = db.password
        self.DB_HOST = db.hostname
        self.DB_PORT = db.port
        self.DB_SSL = 'require'

        # Secrets
        self.RSA_PRIVATE_KEY = os.environ.get("RSA_PRIVATE_KEY")
        self.SECRET_KEY: str = os.environ.get("SECRET_KEY")
        self.SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

        # Gmail login for sending account verification
        self.MAIL_USERNAME = os.environ.get("VERIFICAITON_SENDER_MAIL")
        self.MAIL_PASSWORD = os.environ.get("VERIFICAITON_SENDER_PASSWORD")

        # Mail server
        self.MAIL_SERVER = 'smtp.googlemail.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_TLS = False
        self.MAIL_USE_SSL = True
        
        #0 is substituted for confirm mail link
        self.MAIL_VERIFICATION_HTML = "Welcome to Transaticka! Click on the link to confirm your email: \n{0}"
        self.EXAMPLE_ACCOUNTS = ["pelle", "coolguy", "plutten", "gangstern", "korven"]

class LocalConfig():
    def __init__(self) -> None:
        super().__init__()

        # PostgreSQL
        self.DB_NAME: str = 'postgres'
        self.DB_USER: str = 'postgres'
        self.DB_PASSWORD: str = '123'
        self.DB_HOST: str = None
        self.DB_PORT: int = None
        self.DB_SSL: str = None

        # Secrets
        self.RSA_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
                                MIIBOwIBAAJBAM7UHgUMpbCI0jVyknGrEckIV6UPvocRCts6+xwMzKvearBYVVMF
                                Ctp53K4qH4l3Jsf/J7j8vNlPuOnOVTQ8Z5UCAwEAAQJBALoH+nRqOsG9Xu2p/uR0
                                jUu30DVsIuATySMFOwWw0YsnpegD+R3CADGkV4WU7XWC1pnkPKqktW+8m6yqF10u
                                U+ECIQDqJ/lKU099z9/UyYHTvB+Yw+XReB8ouZh7sdoPC28CXQIhAOIfhGZetq9E
                                7J5miKQBErptcezMy8W+ZnWu/mE8cBaZAiBdnsvqbrLar7Fjp4mz+YR8lN6fSLLU
                                mpgf5LU1zLF+tQIhAIvhDUk6W+4uR+Vw7iPuGgTDQU9IHOH1d3JjTy8dcQU5AiBt
                                c5K4SsYdujRuo8GT8ykwTQRrDpgbywaFYpGBeRnzMA==
                                -----END RSA PRIVATE KEY-----"""
        
        self.SECRET_KEY: str = 'secret'
        self.SECURITY_PASSWORD_SALT = 'secret'
        self.MAIL_USERNAME = 'transaticka.project.test@gmail.com'
        self.MAIL_PASSWORD = 'purpletree1'
        
        # Mail server
        self.MAIL_SERVER = 'smtp.googlemail.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_TLS = False
        self.MAIL_USE_SSL = True

        #0 is substituted for confirm mail link
        self.MAIL_VERIFICATION_HTML = "{0}"