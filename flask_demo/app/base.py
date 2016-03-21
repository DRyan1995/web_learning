from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("./configs/my_config.py")

db = None

db = SQLAlchemy(app)
