import os
from app.common.config import Config
# class NoPositionBucketError(Exception):
#     def __init__(self, content):


class ReadPositionBook:
    """
    """
    def __init__(self, api, instrument="EUR_USD"):
        self.api = api
        self.instrument = instrument
        self.kwargs = {}

    def fetch_position_book(self):
        response = self.api.instrument.position_book(self.instrument)

        if response.status != 200:
            print(response)
            print(response.body)
            return

        position_book = response.get("positionBook", 200)
        position_bucket = position_book.buckets

        long_percentage_total = sum(map(lambda element: element.longCountPercent, position_bucket))



        short_percentage_total = sum(map(lambda element: element.shortCountPercent, position_bucket))

        print("LONG PERCENTAGE TOTAL")
        print(long_percentage_total)
        print("SHORT PERCENTAGE TOTAL")
        print(short_percentage_total)

        """
        "price": "80.900",
        "longCountPercent": "0.0106",
        "shortCountPercent": "0.0000"
        """
if __name__ == "__main__":
    os.environ["TESTING"] = "TRUE"
    ctx = Config()
    ctx.load()
    ctx.validate()
    api = ctx.create_context()
    rpb = ReadPositionBook(api)
    rpb.fetch_position_book()
