from flask import Flask
from flask_login import LoginManager

login_manager = LoginManager()
app = Flask(__name__)