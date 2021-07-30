from flask import Blueprint, request, jsonify
from key_gen import get_lazy_public_key

index = Blueprint('index', __name__)

@index.route('', methods=['GET'])
def get():
    return get_lazy_public_key().export_key().decode('utf-8'), 200