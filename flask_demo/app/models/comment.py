from app.base import db
from .base_model import BaseModel

class Comment(BaseModel):
    page_name = db.Column(db.String(30), index=True)
    author_name = db.Column(db.String(20))
    content = db.Column(db.Text, default="")
    email = db.Column(db.String(30), default="")
    timestr = db.Column(db.String(30), default="")
