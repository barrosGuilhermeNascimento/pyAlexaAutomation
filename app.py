from flask import Flask, Response, request
from datetime import datetime, time, timedelta
from models import universityModel
from functions import university, initialization

classFile = initialization.Init()


app = Flask(__name__)


# Universiry Controllers
@app.route("/university/nextClass")
def nextClassEndPoint():
    try:
        funcResponse = university.nextClass(classFile)
        return Response(funcResponse, 200)
    except Exception as err:
        return Response(f"There was an error in your request: {err}", 500)

@app.route("/university/nowClass")
def nowClass():
    try:
        funcResponse = university.currentClass(classFile)
        return Response(funcResponse, 200)
    except Exception as err:
        return Response(f"There was an error in your request: {err}", 500)
    
@app.route("/university/smartQuestion", methods=["POST"])
def smartQuestions():
    try:
        funcReponse = university.GetClassesDayOrder()
        return Response(funcReponse, 200)
    except Exception as err:
        return Response(f"There was an error in your request: {err}", 500)
    

# Trello Controllers

    
    
# Basic Test
@app.route("/test")
def test():
    return Response("1", 200)    
    


app.run("192.168.15.190", debug=True, port=5070)