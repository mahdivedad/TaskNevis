from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import re

app = Flask(__name__)

Base = declarative_base()

class USER(Base):

    __tablename__ = "users"

    Username = Column("username", String, primary_key=True)
    email = Column("email", String)
    password = Column("password", String)

    def __init__(self, Username, email, password):
        self.Username = Username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"({self.Username}) {self.email} {self.password}"
    
engine = create_engine("sqlite:///users.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

def validemail(input):
    return bool(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',input))
def validuser(input):
    result = session.query(USER).filter(USER.Username == input)
    for r in result:
        return True
    return False
def validlogin(username , password):
    result = session.query(USER).filter(USER.Username == username , USER.password == password)
    for r in result:
        return True
    return False

@app.route("/")
def index():
    return render_template("home.html")

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
        return "You are registered"
    return render_template("register.html")

@app.route("/login", methods=["GET" , "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if validlogin(username , password):
            return "<h1>Welcome</h1>"
        else:
            return render_template("login.html" , invalid=True)
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)