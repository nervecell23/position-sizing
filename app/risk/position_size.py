import os
from app.common.config import Config
from app.risk.atr import ATR
from datetime import datetime


class FetchBaserateError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"


class APIRequestError(Exception):
    pass


class FetchBalanceError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"{self.msg}"


class InvalidGranularity(Exception):
    def __init__(self, granularity):
        self.granularity = granularity

    def __str__(self):
        return f"{self.granularity} is not a valid granularity"


class PositionSize:

    SAXO_BALANCE = 18295.38
    FOREX_BALANCE = 237.69
    DEFAULT_GRANULARITY = 'D'

    def __init__(
            self,
            ctx,
            api,

            saxo_balance=SAXO_BALANCE,
            forex_balance=FOREX_BALANCE,
            default_granularity=DEFAULT_GRANULARITY):

        self.default_granularity = default_granularity
        self.api = api
        self.ctx = ctx
        self.atr = ATR(api=self.api)
        self.balance_gbp = None
        self.balance_usd = None
        self.current_atr = None
        self.position_size_gbp = None
        self.position_size_usd = None
        self.error = None

        # exchange rate between base currency (GBP) and purchasing currency for a pair. e.g. For EURUSD, USD is the purchasing currency
        self.latest_baserate_time = None
        self.latest_baserate = None
        self.saxo_balance = saxo_balance
        self.forex_balance = forex_balance

    # main work here

    def calculate_position_size(self, ticker, atr_multiply_coe=2.0,
                                single_loss_percent=0.03, **kwargs):
        """
        This function calculates position size for two platform. One for GBP account, the other for USD account.

        args:
        ticker -  In the form of "EUR_USD"
        granularity - 
        **kwargs - 
            manual_balance_gbp - if this field is included, then account balance will not be fetched through platform API.
        """
        granularity = kwargs.get("granularity", None)
        print(kwargs)
        print(granularity)
        if granularity == None:
            granularity = self.default_granularity
        self.error = None
        self._validate_granularity(granularity)
        self.target_ticker = ticker
        self.current_atr = self.atr.calculate_atr(ticker, granularity)

        # Handle GBP account
        self.baserate_ticker = self._get_baserate_ticker(ticker)
        try:
            self._fetch_baserate(self.baserate_ticker)
        except FetchBaserateError as error:
            self.error = error
        manual_balance_gbp = kwargs.get("manual_balance_gbp", None)
        if manual_balance_gbp:
            self.balance_gbp = manual_balance_gbp
        else:
            self._fetch_total_balance()
        self.position_size_gbp = self.balance_gbp * single_loss_percent * \
            self.latest_baserate / (self.current_atr * atr_multiply_coe)

        # Handle USD account
        self.baserate_ticker = self._get_baserate_ticker(
            ticker, base_ticker='USD')
        self._fetch_baserate(self.baserate_ticker)
        manual_balance_usd = kwargs.get('manual_balance_usd', None)
        if manual_balance_usd == None:
            raise Exception('USD account balance must be provided')
        self.balance_usd = manual_balance_usd

        print("=================")
        print(manual_balance_usd)
        print(self.balance_usd)
        print(self.latest_baserate)
        print(self.current_atr)

        self.position_size_usd = self.balance_usd * single_loss_percent * \
            self.latest_baserate / (self.current_atr * atr_multiply_coe)

    def _get_baserate_ticker(self, ticker, base_ticker="GBP"):
        purchase_currency = ticker.split("_")[1]
        return "_".join([base_ticker, purchase_currency])

    def _validate_granularity(self, granularity):
        acceptable_granularity = ["S5", "S10", "S15", "S30", "M1", "M2", "M4", "M5",
                                  "M10", "M15", "M30", "H1", "H2", "H3", "H4", "H6", "H8", "H12", "D", "W", "M"]
        if granularity not in acceptable_granularity:
            raise InvalidGranularity(granularity)

    def _fetch_total_balance(self):
        account_id = self.ctx.active_account
        response = self.api.account.summary(account_id)

        response_status = response.status
        if response_status != 200:
            msg = response.body["errorMessage"]
            raise FetchBalanceError(msg)
        self.balance_gbp = response.get(
            "account").balance + self.saxo_balance + self.forex_balance

    def _is_same_ticker(self, ticker):
        temp = ticker.split('_')
        if temp[0] == temp[1]:
            self.latest_baserate = 1.0
            return True
        else:
            return False

    def _fetch_baserate(self, instrument):
        self.latest_baserate_time = None
        self.latest_baserate = None
        if self._is_same_ticker(instrument):
            return
        response = self.api.pricing.get(
            accountID=self.ctx.active_account, instruments=instrument, since=self.latest_baserate_time)
        if response.status != 200:
            raise FetchBaserateError(response.body["errorMessage"])
        prices = response.get("prices", 200)
        for price in prices:
            if self.latest_baserate_time == None or price.time > self.latest_baserate_time:
                self.latest_baserate_time = price.time
                self.latest_baserate = (
                    price.bids[0].price + price.asks[0].price) / 2.0
        if not self.latest_baserate_time:
            raise FetchBaserateError("baserate is None")

    def output_result(self):
        r = {}
        r["balance_gbp"] = self.balance_gbp
        r['balance_usd'] = self.balance_usd
        r["account_number"] = self.ctx.active_account
        r["atr"] = self.current_atr
        r["position_size_gbp"] = self.position_size_gbp
        r['position_size_usd'] = self.position_size_usd
        r["target_ticker"] = self.target_ticker
        return r

    def print_result(self):
        print(f"Active account: {self.ctx.active_account}")
        print(f"-> Current balance (GBP): {self.balance_gbp}")
        print("---------------------------------------------------")
        print(f"Target ticker: {self.target_ticker}")
        print(f"-> Current ATR({self.atr.period}): {self.current_atr:.5f}")
        print(f"-> Position Size: {self.position_size_gbp:.1f}")


if __name__ == "__main__":
    os.environ["TESTING"] = "TRUE"
    ctx = Config()
    ctx.load()
    ctx.validate()
    api = ctx.create_context()
    ps = PositionSize(ctx, api)
    ps.calculate_position_size(
        "EUR_GBP", "H8", **{"manual_balance_gbp": 31145.09})
    ps.print_result()
