import time
import uuid
from peewee import *

proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = proxy

class Account(BaseModel):
    uuid = UUIDField(primary_key=True, default=uuid.uuid4)   
    email = CharField(null=False, unique=True)
    display_name = CharField(null=False, unique=True)
    password_hash = CharField(null=False)
    is_admin = BooleanField(default=False)
    email_confirmed = BooleanField(default=False)
    created_timestamp = IntegerField (default=time.time)

