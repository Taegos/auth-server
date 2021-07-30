from Crypto.PublicKey import RSA

_private_key = None
_public_key = None

def _generate_key_pair_on_disk():
    key_pair = RSA.generate(2048)
    with open('private_key.pem', 'wb') as file:
        file.write(key_pair.export_key())
    with open('public_key.pem', 'wb') as file:
        file.write(key_pair.publickey().export_key())

def get_lazy_private_key() -> RSA.RsaKey:
    global _private_key
    if _private_key is not None:
        return _private_key
    try:
        with open('private_key.pem', 'r') as file:
            _private_key = RSA.import_key(file.read())
            return get_lazy_private_key()       
    except IOError as e:
        print('Private key was not found on disk, generating new key pair...')
        _generate_key_pair_on_disk()
        return get_lazy_private_key()
    
def get_lazy_public_key() -> RSA.RsaKey:
    global _public_key
    if _public_key is not None:
        return _public_key
    try:
        with open('public_key.pem', 'r') as file:
            _public_key = RSA.import_key(file.read())
            return get_lazy_public_key()
    except IOError as e:
        print('Public key was not found on disk, generating new key pair...')
        _generate_key_pair_on_disk()
        return get_lazy_public_key()

