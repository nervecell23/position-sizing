from app import ps_app, ps
from werkzeug.exceptions import BadRequest
from flask import request
# a random comment


@ps_app.route("/")
def hello():
    return "Humble Money Management Tool"


@ps_app.route("/position_size")
def position_size():
    kwargs = {}
    ticker = request.args.get("ticker")
    granularity = request.args.get("granularity")
    manual_balance_gbp = request.args.get("manual_balance_gbp")
    manual_balance_usd = request.args.get('manual_balance_usd')
    print('===================')
    print(manual_balance_gbp)
    print(manual_balance_usd)
    print('===================')
    if manual_balance_gbp != '' and manual_balance_gbp != None:
        kwargs = {"manual_balance_gbp": float(manual_balance_gbp)}
    if manual_balance_usd == '' or manual_balance_usd == None:
        raise BadRequest('Balance of USD account must be provided')
    else:
        kwargs['manual_balance_usd'] = float(manual_balance_usd)
    ps.calculate_position_size(ticker, granularity, **kwargs)
    result = ps.output_result()
    return result, 200


@ps_app.route("/oanda_fees")
def oanda_fees():
    pass


@ps_app.route("/etoro_fees")
def etoro_fees():
    pass

# Error handler


@ps_app.errorhandler(BadRequest)
def bad_request_handler(e):
    return str(e), 400


if __name__ == '__main__':
    ps_app.run()
