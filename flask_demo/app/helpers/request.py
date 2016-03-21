from app.base import app, db

@app.route("/")
def index():
    db.create_all()
    return "success"
