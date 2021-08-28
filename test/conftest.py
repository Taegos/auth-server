from typing import Set
from test.settings import Settings
from config import LocalConfig
import time
import pytest
from multiprocessing import Process

import db
from app import create_local_app

def _start_app(config, host, port):
    app = create_local_app(config)
    app.run(host=host, port=port)

@pytest.fixture(scope='session')
def settings():
    config: LocalConfig = LocalConfig()
    host = 'localhost'
    port = 5001
    process = Process(target=_start_app, args=(config, host, port))
    process.start()
    db.connect(config)
    time.sleep(1)

    settings: Settings = Settings(
        f"http://{host}:{port}",
        config.MAIL_USERNAME
    )

    yield settings
    process.kill()
    db.reset()

@pytest.fixture(autouse=True)
def before_each():
    db.reset()
    yield