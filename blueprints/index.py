from flask import Blueprint, request, render_template
from key_gen import get_lazy_public_key
from db import db

index = Blueprint('index', __name__)

@index.route('', methods=['GET'])
def get():
    data = {
        'public_key': get_lazy_public_key().export_key().decode('utf-8'),
        'accounts': db.accounts.find({})
    }
    return render_template('index.html', data=data)