import collections

class InputCandleError(Exception):
    def __init__(self, candle_list):
        self.candle_list = candle_list

    def __str__(self):
        return "Not enough candles for creating ATR, requires 15 but {} are given".format(len(self.candle_list))

class ATR:
    """
    Using simple moving average for smoothing
    """
    def __init__(self):
        self.candle_list = None
        self.tr_list = []
        
    def calculate_atr(self, candle_list):
        self.candle_list = candle_list

        if len(self.candle_list) < 15:
            raise InputCandleError(self.candle_list)

        length = len(self.candle_list)
        candle_pairs = zip(self.candle_list[0, length-1], self.candle_list[1, length])

        for prev_candle, curr_candle in candle_pairs:
            tr = max(curr_candle.high - curr_candle.low,
                        abs(curr_candle.high - prev_candle.close),
                        abs(curr_candle.low - prev_candle.close))
            self.tr_list.append(tr)

        return sum(self.tr_list) / 15
