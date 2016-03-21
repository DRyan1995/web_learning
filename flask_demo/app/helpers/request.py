from app.base import app, db
from flask import request, url_for, redirect, render_template
from app.models.comment import Comment
from datetime import datetime

@app.route("/")
def index():
    db.create_all()
    cs = Comment.query.all()
    comments = list()
    for c in cs:
        comments.append(c.to_dict())
    print(comments)
    return render_template("comment.html", comments=comments)

@app.route("/comment/commit", methods=["POST"])
def post_comment_commit():
    # print(11)
    page_name = request.form.get("page_name")
    author_name = request.form.get("author_name")
    content = request.form.get("content")
    email = request.form.get("email")
    c = Comment(
        page_name = page_name,
        author_name = author_name,
        content = content,
        email = email
    )
    db.session.add(c)
    db.session.commit()
    return redirect(url_for("index"))
