from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from key_gen import get_lazy_private_key, get_lazy_public_key
import time
import binascii
import json

def generate_token(user_id):
    payload = {
        'created_at': int(time.time()),
        'subject': str(user_id),
    }
    
    h = SHA256.new(json.dumps(payload, separators=(',', ':')).encode('utf-8'))
    signature = pkcs1_15.new(get_lazy_private_key()).sign(h)
    
    token = {
        'payload': payload,
        'signature': binascii.hexlify(signature).decode('ascii')
    }
    
    return token