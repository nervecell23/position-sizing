from app import app, random_message

@app.route("/")
def hello():
    # return "Humble Money Management Tool"
    return random_message

@app.route("/position_size")
def position_size():
    return random_message + ' position_size'

@app.route("/oanda_fees")
def oanda_fees():
    return random_message + ' oanda fees'

@app.route("/etoro_fees")
def etoro_fees():
    return random_message + ' etoro fees'

if __name__ == '__main__':
    app.run()
