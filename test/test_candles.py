import pytest
from app.common.config import Config
from app.risk.candles import Candles
from datetime import datetime
from unittest.mock import patch, Mock, MagicMock 

class TestCandles:
    @pytest.fixture
    def make_mock_candle(self):
        def _make_mock_candle(mid, dt):
            m = Mock()
            m.mid = mid
            m.time = dt
            m.complete = True
            return m
        return _make_mock_candle

    @pytest.fixture
    def mock_response(self, make_mock_candle):
        # instantiate two mock candles
        c1 = make_mock_candle(1.23, datetime(2020, 8, 1).timestamp())
        c2 = make_mock_candle(2.25, datetime(2020, 8, 3).timestamp())

        mock_response = Mock()
        mock_response.status = 200
        mock_response.__str__ = Mock(return_value='response text')
        mock_response.body = Mock()
        mock_response.body.__str__ = Mock(return_value='response body text')
        mock_response.get = Mock(return_value=[c1, c2])
        return mock_response

    def test_fetch_candles(self, mock_response):
        mock_api = Mock()
        mock_api.instrument.candles = Mock(return_value=mock_response)
        subject = Candles(api=mock_api)
        _ = subject.fetch_candles('EUR_USD', 3, 'H8')
        mock_api.instrument.candles.assert_called_once_with(
            'EUR_USD',
            granularity='H8',
            count=3
        )

    def test_candles_get_updated(self, mock_response, make_mock_candle):
        mock_api = Mock()
        mock_api.instrument.candles = Mock(return_value=mock_response)
        subject = Candles(api=mock_api)
        result_updated_time, result_candle_list = subject.fetch_candles('EUR_USD', 3, 'H8')
        expected_updated_time = datetime(2020, 8, 3)
        expected_candle_list = [1.23, 2.25]
        assert result_updated_time == expected_updated_time 
        assert result_candle_list == expected_candle_list

    def test_bad_status_code(self, mock_response, capsys):
        mock_response.status = 400
        mock_api = Mock()
        mock_api.instrument.candles = Mock(return_value=mock_response)
        subject = Candles(api=mock_api)
        _ = subject.fetch_candles('EUR_USD', 3, 'H8')
        out, _ = capsys.readouterr()
        assert out == "response text\nresponse body text\n"




