import binascii
import time
from flask import current_app
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def get_public_key():
    private_key: str = current_app.config['RSA_PRIVATE_KEY']
    return RSA.import_key(private_key).publickey().export_key()

def sign_payload(payload: dict):
    payload['timestamp'] = int(time.time())
    values = ''.join(str(value) for value in list(payload.values()))
    digest = SHA256.new(values.encode('utf-8'))
    private_key = RSA.import_key(current_app.config['RSA_PRIVATE_KEY'])
    signature = pkcs1_15.new(private_key).sign(digest)
    signed = {
        'payload': payload,
        'signature': binascii.hexlify(signature).decode('ascii')
    }
    return signed
