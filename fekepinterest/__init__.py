from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///capfekepinterest.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "https://capfekepinterest.onrender.com.db"
app.config["SECRET_KEY"] = "649be41474027686d97754a466a24bead818b92b2030b4d9"
app.config["UPLOAD_FOLDER"] = "static/fotos_posts"


database = SQLAlchemy(app)
bcrytp = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"

from fekepinterest import routes