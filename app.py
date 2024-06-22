from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import USER,TASK,Base,engine,session
from Functions import validemail,validuser,inuseemail,ValidTaskAdd,validlogin,validEdit,anyData,uniqueData,deleteTask
from config import Add
import re

app = Flask(__name__)

temp = {}

Base = declarative_base()

engine = create_engine(Add, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
                

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not validemail(email):
            return render_template("register.html", invalidemail = True)
        if validuser(username):
            return render_template("register.html", invaliduser = True)
        if inuseemail(email):
            return render_template("register.html", inuseemail=True)
        user = USER(username, email, password)
        session.add(user)
        session.commit()
        temp["username"] = username
        return redirect(url_for("mainpage"))
    return render_template("register.html")


@app.route("/login", methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if validlogin(username , password):
            temp["username"] = username
            return redirect(url_for("mainpage"))        
        return render_template("login.html" , invalid = True)
    return render_template("login.html")


@app.route("/mainpage", methods=["GET", "POST"])
def mainpage():
    if "username" in temp:
        username = temp["username"]
        temp.clear()
        task = session.query(TASK).filter(TASK.owner == username).all()
        return render_template("mainpage.html", username = username, task = task)
    if request.method == "POST":
        action = request.form.get("x")
        username = request.form.get("username")
        task = session.query(TASK).filter(TASK.owner == username).all()
        if action == "add":
            return render_template("Task.html", username = username)
        elif action == "change":
            return render_template("changepassword.html", username = username)
        elif action == "editTask":
            username = request.form.get("username")
            TaskName = request.form.get("task")
            Task = request.form.get("describtion")
            return render_template("EditTasks.html", username = username ,TaskName = TaskName, Task = Task)
        elif action == "deleteTask":
            Taskname = request.form.get("task")
            deleteTask(Taskname,username)
            task = session.query(TASK).filter(TASK.owner == username).all()
            return render_template("mainpage.html", username = username, task = task)
        task = session.query(TASK).filter(TASK.owner == username).all()
        return render_template("mainpage.html", username = username, task = task)
    return redirect("/")

@app.route("/changepassword", methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        username = request.form.get("username")
        currentpassword = request.form.get("current password")
        newpassword = request.form.get("new password")
        if validlogin(username, currentpassword):
            user = session.query(USER).filter(USER.username == username).first()
            user.password = newpassword
            session.commit()
            return redirect(url_for("login"))
        return render_template("changepassword.html", invalid = True, username = username)
    return redirect("/")



@app.route("/Task", methods=["POST","GET"])
def Task():
    if request.method == "POST":
        task=request.form.get("TaskName")
        description = request.form.get("Task")
        owner = request.form.get("Username")
        Condition=request.form.get("condition")
        if ValidTaskAdd(task,owner):
            return render_template("Task.html" , invalid = "There is a Task with this name. please set another name for your new task", username = owner)  
        task = TASK(task, description, owner,Condition)
        session.add(task)
        session.commit()
        task = session.query(TASK).filter(TASK.owner == owner).all()
        return render_template("mainpage.html",username = owner, task = task)
    return redirect("/")


@app.route("/EditingCheck" , methods=["POST","GET"])
def editingcheck():
    if request.method == "POST":
        username = request.form.get("username")
        TaskName = request.form.get("TaskName")
        NewTaskName = request.form.get("NewTaskName")
        Task = request.form.get("describtion")
        Condition = request.form.get("condition")
        if NewTaskName != TaskName and uniqueData(NewTaskName,username):
            return render_template("EditTasks.html", username = username , a = "There is a Task with this name please select another name" , TaskName = TaskName , Task = Task)
        if anyData(TaskName,username):
            Edit = session.query(TASK).filter(TASK.owner == username , TASK.task == TaskName).first()
            Edit.task = NewTaskName
            Edit.describtion = Task
            Edit.Condition = Condition
            session.commit()
            TaskName = NewTaskName
            return render_template("EditTasks.html", username = username , a = "edited successfully!" , TaskName = TaskName , Task = Task)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=False)