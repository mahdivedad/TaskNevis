from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from mothers import USER,TASK,Base,engine,session
from config import Add
import re

Base = declarative_base()

engine = create_engine(Add, echo=True)
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

def inuseemail(email):
    result = session.query(USER).filter(USER.email == email)
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