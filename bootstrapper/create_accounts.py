from models.account import Account
import bcrypt

def _create_account(display_name: str):
    Account.create(
        email=f'{display_name.lower()}@example.com',
        display_name=display_name,
        password_hash=bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
        email_confirmed=True,
        is_admin=True
    )


def create_accounts(*display_names):
    for display_name in display_names:
        _create_account(display_name)