from models.account import Account, proxy
from peewee import PostgresqlDatabase

_db: PostgresqlDatabase = None

def connect(config) -> None:
    db = PostgresqlDatabase(
        config.DB_NAME,
        user=config.DB_USER, 
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        sslmode=config.DB_SSL)
    proxy.initialize(db)
    global _db
    _db = db

def reset():
    global _db
    if _db == None:
        raise Exception("Not connected to db")
    try:
        _db.drop_tables([Account])
        _db.create_tables([Account])
    except Exception:
        pass