from flask_website.config import admin_id, admin_username, admin_password


class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def get_by_id(id):
        if id == admin_id:
            User(admin_id, admin_username, admin_password)
        else:
            return None