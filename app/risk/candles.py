"""
This class has a method that fetch 15 candles from endpoint
"""
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

        if response.status != 200:
            print(response)
            print(response.body)
            return

        candles = response.get("candles", 200)
        for candle in candles:
            candle_list.append(candle.mid)

        return candle_list
