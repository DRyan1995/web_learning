from app.base import app, db
from flask import request, url_for, redirect, render_template
from app.models.comment import Comment
from datetime import datetime
import time

@app.route("/<pageid>", methods=["GET"])
def index(pageid):

    # db.create_all()
    # page_name = request.args.get("page_name")
    # if not page_name:
    #     return "ERROR"
    print(pageid)
    cs = Comment.query.all()
    comments = list()
    for c in cs:
        comments.append(c.to_dict())
    # print(datetime.now())
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
        email = email,
        timestr = time.strftime("%H:%M:%S on %Y-%m-%d",time.localtime(time.time()))
    )
    print(c.timestr)
    db.session.add(c)
    db.session.commit()
    return redirect(url_for("index"))
