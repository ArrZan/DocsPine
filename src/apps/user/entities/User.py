import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, username, password, fullname="", email="", image="", idioma=1) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
        self.image = image
        self.idioma = idioma

    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    def generate_password(self, password):
        return generate_password_hash(password)

    def get_image(self):
        if self.image:
            return f'img/perfil/{self.image}'
        else:
            return f'img/perfil/default.jpg'