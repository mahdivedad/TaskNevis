from flask import Flask, render_template, request, redirect, url_for,session
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re
import os
from IPython.display import HTML

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
    description = Column("describtion", String)
    owner = Column("owner",String)
    Date = Column("Date",String,primary_key=True)
    Time = Column("Time",String)
    Condition=Column("Condition",String)

    def __init__(self, task, describtion, owner, Date, Time, Condition):
        self.task = task
        self.description = describtion
        self.owner = owner
        self.Date = Date
        self.Time = Time
        self.Condition = Condition
    
    

    def __repr__(self):
         html= f"""
         <table border="1">
              <tr>
                  <th>Task</th>
                  <th>Description</th>
                  <th>Owner</th>
                  <th>Date</th>
                  <th>Time</th>
                  <th>Condition</th>
              </tr>
              <tr>
                  <td>{self.task}</td>
                  <td>{self.description}</td>
                  <td>{self.owner}</td>
                  <td>{self.Date}</td>
                  <td>{self.Time}</td>
                  <td>{self.Condition}</td>
              </tr>
         </table>
         """
         return (html)

  
         

    # def __repr__(self):
    #      return f"[{self.task}{self.description} {self.owner} {self.Date} {self.Time} {self.Condition}]"
     
    
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

def validlogin(username , password):
    result = session.query(USER).filter(USER.username == username , USER.password == password)
    for r in result:
        return True
    return False


@app.route("/")
def index():
    return render_template("login.html")


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
        return render_template("mainpage.html", username = username)
    if request.method == "POST":
        action = request.form.get("x")
        username = request.form.get("username")
        if action == "add":
            return render_template("Task.html", username = username)
        elif action == "change":
            return render_template("changepassword.html", username = username)
        else:
            return render_template("mainpage.html", username = username)
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
         description=request.form.get("Task")
         owner=request.form.get("Username")
         Date=request.form.get("DateInput")
         Time=request.form.get("TimeInput")
         Condition=request.form.get("condition")

         
    task = TASK(task, description, owner, Date, Time, Condition)
    session.add(task)
    session.commit()
    return ("Done")



@app.route("/ShowTask", methods=["POST","GET"])
def ShowTask():
    if request.method == "POST":
        ShowTask=request.form.get("ShowTask")
        result = session.query(TASK).filter(TASK.owner == ShowTask).all()
        result =" ".join(map(str, result))
        return render_template("ShowTask.html", rows=result,username=ShowTask)

if __name__ == "__main__":
    app.run(debug=True)