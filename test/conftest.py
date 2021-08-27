import time
import pytest
from multiprocessing import Process

import db
from config import BaseConfig, TestingConfig
from app import create_app

def _start_app(config: BaseConfig):
    app = create_app(config)
    app.run()

@pytest.fixture(scope='session')
def config():
    config = TestingConfig()
    process = Process(target=_start_app, args=(config, ))
    process.start()
    db.connect(config)
    time.sleep(1)
    yield config
    process.kill()
    db.reset()

@pytest.fixture(autouse=True)
def before_each():
    db.reset()
    yield