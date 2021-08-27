from models.account import Account
import bcrypt

def create_example_account(display_name: str):
    Account.create(
        email=f'{display_name.lower()}@example.com',
        display_name=display_name,
        password_hash=bcrypt.hashpw("123456".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
        email_confirmed=True,
        is_admin=True
    )