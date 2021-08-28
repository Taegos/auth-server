from test.settings import Settings
import requests

def test_post_account_ok(settings: Settings):
    res = requests.post(settings.base_url + '/account', json={
        'email': 'benjamin.fischr@gmail.com', 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    })
    assert res.status_code == 201


def test_post_account_bad_format(settings: Settings):
    assert requests.post(settings.base_url + '/account', json={
        'bad': 'benjamin.fischr@gmail.com', 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.post(settings.base_url + '/account', json={
        'email': 'benjamin.fischr@gmail.com', 
        'bad': 'Benji', 
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Benji', 
        'bad': 'dragonslayer'
    }).status_code == 400


def test_post_account_too_short(settings: Settings):
    assert requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Ben',  
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Benji',  
        'password': 'dragons' # Too short
    }).status_code == 400


def test_post_account_unique_fail(settings: Settings):
    requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Benji',  
        'password': 'dragonslayer'
    })

    assert requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.mail', # Email already exists
        'display_name': 'Benji1',  
        'password': 'dragonslayer'
    }).status_code == 409

    assert requests.post(settings.base_url + '/account', json={
        'email': 'mail@mail.mail1',
        'display_name': 'Benji', # Display name already exists
        'password': 'dragonslayer'
    }).status_code == 409
