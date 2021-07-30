from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from key_gen import get_lazy_private_key
import time

def generate_token(user_id):
    token = {
        'created_at' : int(time.time()),
        'subject' : str(user_id),
    }

    digest = SHA256.new(str(token).encode('utf-8'))
    signature = pkcs1_15.new(get_lazy_private_key()).sign(digest)
    token['signature'] = signature.hex()
    return token