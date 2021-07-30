from peewee import *
from db import db

class BaseModel(Model):
    class Meta:
        database = db

class Account(BaseModel):
    email = CharField(unique=True)
    password_hash = CharField()