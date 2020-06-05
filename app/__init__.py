import os

from instance.config import Config
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

from app.common.config import Config as AppCfg
from app.risk.position_size import PositionSize

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

from app.models import users

# create OANDA V20 api and context
os.environ["TESTING"] = "TRUE"
ctx = AppCfg()
ctx.load()
ctx.validate()
api = ctx.create_context()
ps = PositionSize(ctx, api)
random_message = "Hello :)"
