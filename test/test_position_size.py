import pytest
from unittest.mock import Mock
from app.risk.position_size import PositionSize, InvalidGranularity

@pytest.fixture
def subject():
    return PositionSize(ctx=None, api=None)

def test_get_baserate_ticker(subject):
    result = subject._get_baserate_ticker("USD_JPY")
    expected = "GBP_JPY"
    assert result == expected

def test_invalid_granularity_exception(subject):
    with pytest.raises(InvalidGranularity):
        subject.calculate_position_size("EUR_USD", "8H")
