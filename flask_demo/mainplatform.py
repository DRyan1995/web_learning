from flask import Flask, redirect, url_for, render_template, send_from_directory
from flask import request
import time

app = Flask(__name__)
database = list()

@app.route("/index")
def index():
    get_current_time()
    timedata = dict(time = get_current_time())
    return render_template("base.html", datas = database, timedata = timedata)

@app.route("/login")
def login():
    return "Please Login"

@app.route("/user/<username>")
def profile(username):
    return redirect(url_for("hello",name=username))

@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    if name:
        print("%s logged in!"%name)
        return "Hello %s" % name
    return "Hello!"

@app.route("/images/<imgname>")
def get_img(imgname):
    return send_from_directory('static', filename=imgname)

#Using GET method
@app.route("/item/commit", methods=["GET", "POST"])
def commit_item():
    if request.method == "GET":
        datas = dict(
            index = database.__len__(),
            name = request.args.get("name"),
            time = request.args.get("time"),
            mission = request.args.get("mission")
            )
        complete_mission_id = request.args.get("complete_mission_id")

    else:
        print(1111)
        datas = dict(
            index = database.__len__(),
            name = request.form['name'],
            time = request.form["time"],
            mission = request.form["mission"]
        )
        complete_mission_id = request.form.get("complete_mission_id")
    database.append(datas)#add the datas to my database
    complete(complete_mission_id)
    return redirect(url_for('index'))


def complete(mission_id=None):
    # print(mission_id)
    if mission_id:
        for datas in database:
            if datas["index"] == int(mission_id):
                database.remove(datas)
                return

def get_current_time():
    timestr=time.strftime("%H:%M:%S@%Y-%m-%d",time.localtime(time.time()))
    # print(timestr)
    # print(timestr)
    return timestr

if __name__ == '__main__':
    app.debug = True
    app.run()
