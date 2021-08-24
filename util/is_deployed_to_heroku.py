import os

def is_deployed_to_heroku() -> bool:
    return 'DYNO' in os.environ