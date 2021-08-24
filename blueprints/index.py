from flask import Blueprint, render_template

from util.rsa import get_lazy_public_key
from models.account import Account

index = Blueprint('index', __name__)

@index.route('', methods=['GET'])
def get():
    data = {
        'public_key': get_lazy_public_key().export_key().decode('utf-8'),
        'accounts': [account for account in Account.select().order_by(Account.created_timestamp).dicts()]
    }
    return render_template('index.html', data=data)