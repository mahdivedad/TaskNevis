from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import Add

Base = declarative_base()

engine = create_engine(Add, echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

class USER(Base):

    __tablename__ = "users"

    username = Column("username", String, primary_key=True)
    email = Column("email", String)
    password = Column("password", String)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

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