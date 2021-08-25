from peewee import PostgresqlDatabase

_database: PostgresqlDatabase = None

def connect_database(config) -> None:
    global _database
    _database = PostgresqlDatabase(
        config.DB_NAME,
        user=config.DB_USER, 
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT,
        sslmode=config.DB_SSL)

def get_database() -> PostgresqlDatabase:
    if _database is None:
        raise Exception("Database has not been initialized yet")
    return _database