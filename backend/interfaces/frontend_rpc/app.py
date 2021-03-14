from flask import Flask

from interfaces.frontend_rpc.blueprints import auth_blueprint, tg_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint)
app.register_blueprint(tg_blueprint)
