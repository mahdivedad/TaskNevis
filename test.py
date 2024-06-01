from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, We are Mahdi Vedad Mahmooudi,Seyed Mohammad Hossein Hosseini and Behrad Ghasemi</p>"
