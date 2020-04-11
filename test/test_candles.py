import pytest
from app.risk.config import Config
from app.risk.candles import Candles

@pytest.fixture
def api():
    cfg = Config()
    cfg.load()
    return cfg.create_context()

@pytest.fixture
def subject(api):
    subject = Candles(api)
    return subject

def test_fetch_candles(subject):
    result = subject.fetch_candles(15)
    assert len(result) == 15
    for element in result:
        assert type(element.o) is float
        assert type(element.h) is float
        assert type(element.l) is float
        assert type(element.c) is float

    result = subject.fetch_candles(1)
    assert len(result) == 1
    for element in result:
        assert type(element.o) is float
        assert type(element.h) is float
        assert type(element.l) is float
        assert type(element.c) is float
