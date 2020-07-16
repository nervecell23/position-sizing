from app import ps_app, ps
from flask import request
# a random comment
@ps_app.route("/")
def hello():
    # return "Humble Money Management Tool"
    return "Hello!"

@ps_app.route("/position_size")
def position_size():
    kwargs = {}
    ticker = request.args.get("ticker")
    granularity = request.args.get("granularity")
    manual_balance = request.args.get("manual_balance")
    if manual_balance != "":
        kwargs = {"manual_balance": float(manual_balance)}
    ps.calculate_position_size(ticker, granularity, **kwargs)
    result = ps.output_result()
    return result, 200

@ps_app.route("/oanda_fees")
def oanda_fees():
    return random_message + ' oanda fees'

@ps_app.route("/etoro_fees")
def etoro_fees():
    return random_message + ' etoro fees'

if __name__ == '__main__':
    ps_app.run()
