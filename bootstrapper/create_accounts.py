from models.account import Account
import bcrypt

def _create_account(display_name: str):
    try:
        Account.create(
            email=f'{display_name.lower()}@example.com',
            display_name=display_name,
            password_hash=bcrypt.hashpw("123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
            email_confirmed=True,
            is_admin=True
        )
    except Exception:
        pass

def create_accounts(*display_names):
    for display_name in display_names:
        _create_account(display_name)

def create_example_accounts():
    create_accounts(
        'Ghaf',
        'Brind',
        'Alchemight',
        'Incantates',
        'Dreadfuls',
        'Burvalr',
        'Khurkmostroll'
    )