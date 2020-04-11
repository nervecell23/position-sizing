"""
This class has a method that fetch 15 candles from endpoint
"""
from datetime import datetime

class Candles:

    def __init__(self, api, instrument="EUR_USD"):
        self.api = api
        self.instrument = instrument

        self.kwargs = {}
        self.kwargs["granularity"] = "H8"

    def fetch_candles(self, candle_count):
        self.kwargs["count"] = candle_count
        response = self.api.instrument.candles(self.instrument, **self.kwargs)
        candle_list = []
        updated_time = None
        prev_updated_time = datetime.fromtimestamp(0.0)

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

        return (updated_time, candle_list)
