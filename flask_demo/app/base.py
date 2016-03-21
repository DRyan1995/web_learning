from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("./configs/my_config.py")

db = None

db = SQLAlchemy(app)


if __name__ == '__main__':
    port = 7000
    app.run(host="0.0.0.0", port=port, debug=True)
