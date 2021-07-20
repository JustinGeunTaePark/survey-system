from flask import Flask
from flask_login import LoginManager
app = Flask(__name__)
app.config["SECRET_KEY"] = "Highly secret key"
app.config["TESTING"] = False
q_for_survey = []

login_manager = LoginManager()
login_manager.init_app(app)