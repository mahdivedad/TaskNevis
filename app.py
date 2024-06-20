from flask import Flask, render_template, request, redirect, url_for,session
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

app = Flask(__name__)

Base = declarative_base()

temp = {}

class USER(Base):

    __tablename__ = "users"

    username = Column("username", String, primary_key=True)
    email = Column("email", String)
    password = Column("password", String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"({self.username}) {self.email} {self.password}"

class TASK(Base):

    __tablename__ = "tasks"

    task = Column("task", String, primary_key=True)
    describtion = Column("describtion", String)
    owner = Column("owner",String)
    Condition=Column("Condition",String)

    def __init__(self, task, describtion, owner, Condition):
        self.task = task
        self.describtion = describtion
        self.owner = owner
        self.Condition = Condition
     
    
engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()


def validemail(input):
    return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',input))

def validuser(input):
    result = session.query(USER).filter(USER.username == input)
    for r in result:
        return True
    return False

def ValidTaskAdd(task,owner):
    result = session.query(TASK).filter(TASK.task == task and TASK.owner == owner)
    for r in result:
        return True
    return False

def validlogin(username , password):
    result = session.query(USER).filter(USER.username == username , USER.password == password)
    for r in result:
        return True
    return False

def validEdit(username , Taskname):
    result= session.query(TASK).filter(TASK.owner == username , TASK.task == Taskname)
    for r in result:
        return True
    return False

def anyData(TaskName,username):
    result= session.query(TASK).filter(TASK.owner == username , TASK.task == TaskName)
    for r in result:
        return True
    return False

def uniqueData(TaskName,username):
    result = session.query(TASK).filter(TASK.owner == username , TASK.task == TaskName)
    for r in result:
        return True
    return False

def deleteTask(Taskname,username):
        if anyData(Taskname,username):
            result = session.query(TASK).filter(TASK.task == Taskname).first()
            session.delete(result)
            session.commit()


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
        else:
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
        else:
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
        else:
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
            return render_template("Task.html" , invalid = "There is a Task with this name. please set another name for your new task")  
        task = TASK(task, description, owner,Condition)
        session.add(task)
        session.commit()
        task = session.query(TASK).filter(TASK.owner == owner).all()
        return render_template("mainpage.html",username = owner, task = task)
    return redirect("/")
       
     
@app.route("/Backtomainpage" , methods = ["POST","GET"])
def BacktoMainPage():
    if request.method == "POST":
        mainpageusername = request.form.get("username")
        return render_template("mainpage.html",username = mainpageusername)
    return redirect("/")   
         
@app.route("/EditingCheck" , methods=["POST","GET"])
def editingcheck():
    if request.method == "POST":
        username = request.form.get("username")
        TaskName = request.form.get("TaskName")
        NewTaskName = request.form.get("NewTaskName")
        Task = request.form.get("describtion")
        Condition = request.form.get("condition")
        if anyData(TaskName,username):
             Edit = session.query(TASK).filter(TASK.owner == username , TASK.task == TaskName).first()
             Edit.task = NewTaskName
             Edit.describtion = Task
             Edit.Condition = Condition
             session.commit()
             TaskName = NewTaskName
             return render_template("EditTasks.html", username = username , a = "" , TaskName = TaskName , Task = Task)
        else:
            return render_template("EditTasks.html", username = username , a = "There is no Task with This Name" , TaskName = TaskName , Task = Task)
           

if __name__ == "__main__":
    app.run(debug=False)

    
# @app.route("/EditTask",methods=["POST",'GET'])
# def EditTask():
#     username = request.form.get("username")
#     if request.method == "POST":
#         Taskname=request.form.get("NameTask")
#         Task=request.form.get("Task")
#         Condition=request.form.get("Condition")
#         Username=request.form.get("username")
#         if validEdit(Username , Taskname):
#             Task = session.query(TASK).filter(TASK.task == Taskname).first()
#             Task.task = Taskname
#             Task.description = Task
#             Task.Date = None
#             Task.Time = None
#             Task.Condition = Condition
#             db.session.commit()
#             return redirect(url_for("mainpage"))
#     return render_template("EditTasks.html", username = username)
