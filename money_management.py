from app import pos_size_app, random_message, ps
from flask import request
# a random comment
@pos_size_app.route("/")
def hello():
    # return "Humble Money Management Tool"
    return random_message

@pos_size_app.route("/position_size")
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

@pos_size_app.route("/oanda_fees")
def oanda_fees():
    return random_message + ' oanda fees'

@pos_size_app.route("/etoro_fees")
def etoro_fees():
    return random_message + ' etoro fees'

if __name__ == '__main__':
    pos_size_app.run(host="0.0.0.0")
