import os
import time
from peewee import *
from urllib.parse import urlparse

deployed = False
if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    db = urlparse(DATABASE_URL)
    user = db.username
    password = db.password
    path = db.path[1:]
    host = db.hostname
    port = db.port
    database = PostgresqlDatabase(path, user=user, password=password, host=host, port=port, sslmode='require')
    deployed = True
else:
    database = PostgresqlDatabase('postgres', user='postgres', password="123")

class BaseModel(Model):
    class Meta:
        database = database

class Account(BaseModel):
    email = CharField(null=False, unique=True)
    display_name = CharField(null=False, unique=True)
    password_hash = CharField(null=False)
    is_admin = BooleanField(default=False)
    email_confirmed = BooleanField(default=False)
    registered_at = IntegerField (default=(int)(time.time()))

try:
    database.create_tables([Account])
    #if not deployed:
    database.drop_tables(Account)
except IntegrityError:
    pass