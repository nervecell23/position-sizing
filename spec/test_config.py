from ...models.config import Config
import pytest
import os

def test_load():
    "it loads configuration from environment variables"
    os.environ['USERNAME'] = 'test_username'
    os.environ['TOKEN']
    os.environ['ACCOUNTS']
    os.environ['ACTIVE_ACCOUNT']
    subject = Config()
    subject.load()
    assert subject.username == 'test_username'
    assert subject.token == 'test_token'
    assert subject.accounts == ['acc_1', 'acc_2']
    assert subject.active_account == 'acc_2'
