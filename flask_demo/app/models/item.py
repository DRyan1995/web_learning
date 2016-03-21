from app.base import db
from .base_model import HashIdModel

class Item(HashIdModel):
    page_name = db.Column(db.String(30), index=True)
    author_name = db.Column(db.String(20))
    content = db.Column(db.Text, default="")
