import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import DevelopmentConfig
from app.common.config import Config as APIConfig
from app.risk.position_size import PositionSize

app = Flask(__name__)
CORS(app)
app.config.from_object(DevelopmentConfig)
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
