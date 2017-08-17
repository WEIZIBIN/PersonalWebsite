from flask_website.views import chat
from flask_website.views import general
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
login_manager = LoginManager()

app.register_blueprint(chat)
app.register_blueprint(general)