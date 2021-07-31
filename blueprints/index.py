from flask import Blueprint, request, jsonify, render_template
from key_gen import get_lazy_public_key
from account_model import Account

index = Blueprint('index', __name__)

@index.route('', methods=['GET'])
def get():
    data = {
        'public_key': get_lazy_public_key().export_key().decode('utf-8'),
        'accounts': [account for account in Account.select(Account.id, Account.email).order_by(Account.id).dicts()]
    }
    return render_template('index.html', data=data)