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
        self.latest_gbpusd_time = None
        self.latest_gbpusd = None
        self.saxo_balance = saxo_balance
        self.forex_balance = forex_balance


    # main work here
    def calculate_position_size(self):
        self._fetch_gbpusd()
        self._fetch_total_balance()
        current_atr = self.atr.calculate_atr()

        print(f"Active account: {self.ctx.active_account}")
        print(f"-> Current balance: {self.balance}")
        print(f"-> Current GBPUSD: {self.latest_gbpusd:.5f} @ {datetime.fromtimestamp(float(self.latest_gbpusd_time))}")
        print(f"-> Current ATR({self.atr.period}): {current_atr:.5f}")

        position_size = self.balance * self.single_loss_percent * self.latest_gbpusd / (current_atr * self.atr_multiply_coe)

        print(f"-> Position Size: {position_size:.1f}")

    def _fetch_total_balance(self):
        account_id = self.ctx.active_account
        response = self.api.account.summary(account_id)

        response_status = response.status
        if response_status != 200:
            raise FetchBalanceError(response_status)
        self.balance = response.get("account").balance + self.saxo_balance + self.forex_balance

    def _fetch_gbpusd(self):
        response = self.api.pricing.get(accountID=self.ctx.active_account, instruments="GBP_USD", since=self.latest_gbpusd_time)

        if response.status != 200:
            raise FetchBalanceError(response.status, response.body)

        prices = response.get("prices", 200)

        for price in prices:
            if self.latest_gbpusd_time == None or price.time > self.latest_gbpusd_time:
                self.latest_gbpusd_time = price.time
                self.latest_gbpusd = (price.bids[0].price + price.asks[0].price) / 2.0

if __name__ == "__main__":
    os.environ["TESTING"] = "FALSE"
    #os.environ["TESTING"] = "TRUE"
    ctx = Config()
    ctx.load()
    ctx.validate()
    api = ctx.create_context()
    ps = PositionSize(ctx, api)
    ps.calculate_position_size()
