import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.common.config import Config as APIConfig
from app.risk.position_size import PositionSize

app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ["APP_TESTINGS"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# create OANDA V20 api and context
os.environ["TESTING"] = "TRUE"
ctx = APIConfig()
ctx.load()
ctx.validate()
api = ctx.create_context()
ps = PositionSize(ctx, api)
random_message = "Hello :)"
