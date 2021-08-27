import requests

def base_url(config) -> str:
    return f"http://{config.HOST}:{config.PORT}"

def test_post_account_ok(config):
    res = requests.post(base_url(config) + '/account', json={
        'email': 'benjamin.fischr@gmail.com', 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    })
    assert res.status_code == 201


def test_post_account_bad_format(config):
    assert requests.post(base_url(config) + '/account', json={
        'bad': 'benjamin.fischr@gmail.com', 
        'display_name': 'Benji', 
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.post(base_url(config) + '/account', json={
        'email': 'benjamin.fischr@gmail.com', 
        'bad': 'Benji', 
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Benji', 
        'bad': 'dragonslayer'
    }).status_code == 400


def test_post_account_too_short(config):
    assert requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Ben',  
        'password': 'dragonslayer'
    }).status_code == 400

    assert requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Benji',  
        'password': 'dragons' # Too short
    }).status_code == 400


def test_post_account_unique_fail(config):
    requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.mail', 
        'display_name': 'Benji',  
        'password': 'dragonslayer'
    })

    assert requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.mail', # Email already exists
        'display_name': 'Benji1',  
        'password': 'dragonslayer'
    }).status_code == 409

    assert requests.post(base_url(config) + '/account', json={
        'email': 'mail@mail.mail1',
        'display_name': 'Benji', # Display name already exists
        'password': 'dragonslayer'
    }).status_code == 409
