from app import ps_app, ps
from werkzeug.exceptions import BadRequest
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
    manual_balance_gbp = request.args.get("manual_balance_gbp")
    manual_balance_usd = request.args.get('manual_balance_usd')
    if manual_balance_gbp != "":
        kwargs = {"manual_balance": float(manual_balance_gbp)}
    if manual_balance_usd == '':
        #raise error message
        raise BadRequest('Balance of USD account cannot be None')
    ps.calculate_position_size(ticker, granularity, **kwargs)
    result = ps.output_result()
    return result, 200

@ps_app.route('/test')
def test_func():
    raise BadRequest('This is a test')
    return 'This should not be reached'

@ps_app.route("/oanda_fees")
def oanda_fees():
    pass
@ps_app.route("/etoro_fees")
def etoro_fees():
    pass
if __name__ == '__main__':
    ps_app.run()
