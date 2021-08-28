import requests

from test.settings import Settings
from test.random_mail import RandomMail

def test_get_auth_token_ok(settings: Settings):
    mail = RandomMail()
    assert requests.post(settings.base_url + '/account', json={
        'email': mail.email_addr, 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    })

    # Painfully slow
    confirm_link = mail.wait_from(settings.verification_sender)
    assert confirm_link != None
    assert requests.get(confirm_link).status_code == 200
    
    response = requests.get(settings.base_url + '/auth_token', json={
        'email': mail.email_addr, 
        'password': 'dragonslayer'
    })
    
    assert response.status_code == 200

def test_get_auth_token_bad_format(settings: Settings):
    assert requests.get(settings.base_url + '/auth_token', json={
        'bad': 'mail@mail.mail', 
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.get(settings.base_url + '/auth_token', json={
        'email': 'mail@mail.mail', 
        'bad': 'dragonslayer'
    }).status_code == 400


def test_auth_token_not_confirmed_yet(settings: Settings):
    requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.com', 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    })

    assert requests.get(settings.base_url + '/auth_token', json={
        'email':'mail@mail.com', 
        'password': 'dragonslayer'
    }).status_code == 401


def test_auth_token_invalid_credentials(settings: Settings):
    assert requests.get(settings.base_url + '/auth_token', json={
        'email': 'mail@mail.com', 
        'password': 'dragonslayer'
    }).status_code == 401