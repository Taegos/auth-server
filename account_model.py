import os
import urllib.parse
import time
from peewee import *

if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    db = urllib.parse(DATABASE_URL)
    user = db.username
    password = db.password
    path = db.path[1:]
    host = db.hostname
    port = db.port
    database = PostgresqlDatabase(path, user=user, password=password, host=host, port=port, sslmode='require')
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

database.create_tables([Account])