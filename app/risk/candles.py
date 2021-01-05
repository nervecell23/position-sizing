"""
This class has a method that fetch 15 candles from endpoint
"""
from datetime import datetime
from app.common.schema import CandlesWindow


class Candles:
    def __init__(self, api):
        self.api = api
        self.kwargs = {}

    def fetch_candles(self, instrument, candle_count, granularity):
        self.kwargs["granularity"] = granularity
        self.kwargs["count"] = candle_count
        response = self.api.instrument.candles(instrument, **self.kwargs)
        candle_list = []
        updated_time = None
        prev_updated_time = datetime.fromtimestamp(0.0)
        prev_updated_time = 0.0

        if response.status != 200:
            print(response)
            print(response.body)
            return

        candles = response.get("candles", 200)
        for candle in candles:
            updated_time = datetime.fromtimestamp(float(candle.time))
            if candle.complete == True and updated_time > prev_updated_time:
                candle_list.append(candle.mid)
                prev_updated_time = updated_time

        if prev_updated_time == 0.0:
            raise ValueError('Updated time == 0.0')

        result = CandlesWindow(
            updated_time=prev_updated_time,
            granularity=granularity,
            candle_list=candle_list
        )
        return result
