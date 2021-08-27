import time
import requests

class RandomMail:
    def __init__(self) -> None:
        response = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address&lang=en&site=guerrillamail.com&ip=127.0.0.1&agent=Mozilla_foo_bar')
        data = response.json()
        self._sid_token = data['sid_token']
        self.email_addr = data['email_addr']

    def wait_from(self, sender, max_tries=120) -> str:
        tries = 0
        while tries < max_tries:
            time.sleep(1)
            for msg in self._check_email()['list']:
                if msg['mail_from'] == sender:
                    return msg['mail_excerpt']
            tries += 1
        return None

    def _check_email(self) -> dict:
        response = requests.get(f'https://api.guerrillamail.com/ajax.php?f=check_email&seq=0&sid_token={self._sid_token}')
        data = response.json()
        self._sid_token = data['sid_token']
        return data