from app import app, random_message, ps
from flask import request

@app.route("/")
def hello():
    # return "Humble Money Management Tool"
    return random_message

@app.route("/position_size")
def position_size():
    kwargs = {}
    ticker = request.args.get("ticker")
    granularity = request.args.get("granularity")
    manual_balance = request.args.get("manual_balance")
    if manual_balance != "":
        kwargs = {"manual_balance": float(manual_balance)}
    ps.calculate_position_size(ticker, granularity, **kwargs)
    return ps.output_result()
    # return random_message

@app.route("/oanda_fees")
def oanda_fees():
    return random_message + ' oanda fees'

@app.route("/etoro_fees")
def etoro_fees():
    return random_message + ' etoro fees'

if __name__ == '__main__':
    app.run()
