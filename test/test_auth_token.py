from re import purge
import requests

from config import BaseConfig
from test.random_mail import RandomMail

def base_url(config) -> str:
    return f"http://{config.HOST}:{config.PORT}"

def test_get_auth_token_ok(config: BaseConfig):
    mail = RandomMail()
    assert requests.post(base_url(config) + '/account', json={
        'email': mail.email_addr, 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    })

    # Painfully slow
    confirm_link = mail.wait_from(config.MAIL_USERNAME)
    assert confirm_link != None
    assert requests.get(confirm_link).status_code == 200
    
    response = requests.get(base_url(config) + '/auth_token', json={
        'email': mail.email_addr, 
        'password': 'dragonslayer'
    })
    assert response.status_code == 200
    
    #data = response.json()
    #public_key =


def test_get_auth_token_bad_format(config):
    assert requests.get(base_url(config) + '/auth_token', json={
        'bad': 'mail@mail.mail', 
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.get(base_url(config) + '/auth_token', json={
        'email': 'mail@mail.mail', 
        'bad': 'dragonslayer'
    }).status_code == 400


def test_auth_token_not_confirmed_yet(config: BaseConfig):
    requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.com', 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    })

    assert requests.get(base_url(config) + '/auth_token', json={
        'email':'mail@mail.com', 
        'password': 'dragonslayer'
    }).status_code == 401


def test_auth_token_invalid_credentials(config: BaseConfig):
    assert requests.get(base_url(config) + '/auth_token', json={
        'email': 'mail@mail.com', 
        'password': 'dragonslayer'
    }).status_code == 401