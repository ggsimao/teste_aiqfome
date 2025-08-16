from flask import Flask

from src.favorites.favorites import favorites_bp
from src.users.users import users_bp

app = Flask(__name__)
app.register_blueprint(favorites_bp)
app.register_blueprint(users_bp)
