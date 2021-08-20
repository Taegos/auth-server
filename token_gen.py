from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from key_gen import get_lazy_private_key
import time
import binascii

def generate_token(email, display_name, is_admin):
    token = {
        'created_at': int(time.time()),
        'email': email,
        'display_name': display_name,
        'is_admin': is_admin
    }

    values = ''.join(str(value) for value in list(token.values()))    
    digest = SHA256.new(values.encode('utf-8'))
    signature = pkcs1_15.new(get_lazy_private_key()).sign(digest)
    token['signature'] = binascii.hexlify(signature).decode('ascii')
    return token