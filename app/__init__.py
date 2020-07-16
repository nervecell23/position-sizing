from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.common.config import Config as APIConfig
from app.risk.position_size import PositionSize
from app.models import db
from config import Config as APP_DEF_CONFIG

ps_app = Flask(__name__)
CORS(ps_app)
ps_app.config.from_object(APP_DEF_CONFIG)
db.init_app(ps_app)
migrate = Migrate(ps_app, db)

# create OANDA V20 api and context
ctx = APIConfig()
ctx.load()
ctx.validate()
api = ctx.create_context()
ps = PositionSize(ctx, api)
