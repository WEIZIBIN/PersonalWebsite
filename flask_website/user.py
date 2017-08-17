from flask_login import UserMixin
from flask_website.config import admin_username, admin_password


class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def is_authenticated(self):
        pass

    def is_active(self):
        pass

    def is_anonymous(self):
        pass

    def get_id(self):
        pass