import os
from math import ceil
from app.common.config import Config
from app.risk.atr import ATR
from datetime import datetime

class FetchBalanceError(Exception):
    def __init__(self, status, msg):
        self.status = status
        self.msg = msg

    def __str__(self):
        return f"status: {self.status}\ndetails: {self.msg}"

class InvalidGranularity(Exception):
    def __init__(self, granularity):
        self.granularity = granularity

    def __str__(self):
        return f"{self.granularity} is not a valid granularity"



class PositionSize:
    ATR_MULTIPLY_COEFFICIENT = 2.5
    SINGLE_LOSS_PERCENT = 0.02
    SAXO_BALANCE = 18295.38
    FOREX_BALANCE = 237.69

    def __init__(
        self,
        ctx,
        api,
        atr_multiply_coe=ATR_MULTIPLY_COEFFICIENT,
        single_loss_percent=SINGLE_LOSS_PERCENT,
        saxo_balance=SAXO_BALANCE,
        forex_balance=FOREX_BALANCE):

        self.api = api
        self.ctx = ctx
        self.single_loss_percent = single_loss_percent
        self.atr_multiply_coe = atr_multiply_coe
        self.atr = ATR(api=self.api)
        self.balance = None
        self.current_atr = None
        self.position_size = None

        # exchange rate between base currency (GBP) and purchasing currency for a pair. e.g. For EURUSD, USD is the purchasing currency
        self.latest_baserate_time = None
        self.latest_baserate = None

        self.saxo_balance = saxo_balance
        self.forex_balance = forex_balance


    # main work here
    def calculate_position_size(self, ticker, granularity):
        """
        args
        ticker: In the form of e.g. "EUR_USD"
        """
        self._validate_granularity(granularity)
        self.target_ticker = ticker
        self.baserate_ticker = self._get_baserate_ticker(ticker)
        self._fetch_baserate(self.baserate_ticker)
        self._fetch_total_balance()
        self.current_atr = self.atr.calculate_atr(ticker, granularity)
        self.position_size = self.balance * self.single_loss_percent * self.latest_baserate / (self.current_atr * self.atr_multiply_coe)

    def _get_baserate_ticker(self, ticker):
        purchase_currency = ticker.split("_")[1]
        return "_".join(["GBP", purchase_currency])

    def _validate_granularity(self, granularity):
        acceptable_granularity = ["S5", "S10", "S15", "S30", "M1", "M2", "M4", "M5", "M10", "M15", "M30", "H1", "H2", "H3", "H4", "H6", "H8", "H12", "D", "W", "M"]
        if granularity not in acceptable_granularity:
            raise InvalidGranularity(granularity)


    def output_result(self):
        r = {}
        r["balance"] = self.balance
        r["account_number"] = self.ctx.active_account
        r["base_rate"] = self.latest_baserate
        r["base_rate_time"] = self.latest_baserate_time
        r["atr"] = self.current_atr
        r["position_size"] = self.position_size
        r["target_ticker"] = self.target_ticker
        r["baserate_ticker"] = self.baserate_ticker
        return r

    def print_result(self):
        print(f"Active account: {self.ctx.active_account}")
        print(f"-> Current balance: {self.balance}")
        print("---------------------------------------------------")
        print(f"Target ticker: {self.target_ticker}")
        print(f"Baserate ticker: {self.baserate_ticker}")
        print(f"-> Current base rate: {self.latest_baserate:.5f} @ {datetime.fromtimestamp(float(self.latest_baserate_time))}")
        print(f"-> Current ATR({self.atr.period}): {self.current_atr:.5f}")
        print(f"-> Position Size: {self.position_size:.1f}")

    def _fetch_total_balance(self):
        account_id = self.ctx.active_account
        response = self.api.account.summary(account_id)

        response_status = response.status
        if response_status != 200:
            raise FetchBalanceError(response_status)
        self.balance = response.get("account").balance + self.saxo_balance + self.forex_balance

    def _fetch_baserate(self, instrument):
        response = self.api.pricing.get(accountID=self.ctx.active_account, instruments=instrument, since=self.latest_baserate_time)

        if response.status != 200:
            raise FetchBalanceError(response.status, response.body)

        prices = response.get("prices", 200)

        for price in prices:
            if self.latest_baserate_time == None or price.time > self.latest_baserate_time:
                self.latest_baserate_time = price.time
                self.latest_baserate = (price.bids[0].price + price.asks[0].price) / 2.0

if __name__ == "__main__":
    os.environ["TESTING"] = "TRUE"
    ctx = Config()
    ctx.load()
    ctx.validate()
    api = ctx.create_context()
    ps = PositionSize(ctx, api)
    ps.calculate_position_size("USD_JPY", "H8")
    ps.print_result()
