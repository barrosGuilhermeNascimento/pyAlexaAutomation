from flask import Flask, Response, request
from datetime import datetime, time, timedelta
import json

file = open("./classes.json")
classFile: dict = json.load(file)
file.close()

days: dict = {"monday":"1", "tuesday":"2", "wednesday": "3", "thursday": "4", "friday": "5", "saturday": "6", "sunday":"7", "tomorrow": "", "yesterday": "", "today": ""}


app = Flask(__name__)

def getDayClasses(day: int) -> dict:
    todayClasses: dict = classFile[str(day)]
    return todayClasses

def allDayClasses(todayClasses: dict):
    if(todayClasses == None):
        return 'You do not have any classes in the choosen day!'
    stringReturn = "Your today classes are: "
    for i in todayClasses:
        classTime = datetime.strptime(i, "%H:%M").time()
        stringReturn += f''' at {classTime.hour} hours and {classTime.minute} minutes, you have 
            {todayClasses[i]["initials"]} {todayClasses[i]["name"]},
            ministered by {todayClasses[i]['teacher']}, 
        '''
    return stringReturn

@app.route("/nextClass")
def nextClass():
    nowDateTime = datetime.now()
    nowTime = nowDateTime.time()
    weekDay = nowDateTime.isoweekday()
    todayClasses = getDayClasses(weekDay)
    while (weekDay < 6):
        todayClasses: dict = classFile[str(weekDay)]
        for i in todayClasses.keys():
            classTime = datetime.strptime(i, "%H:%M").time()
            if ( nowTime < classTime):
                return Response(
                    f'''Your next Class is: {todayClasses[i]['initials']} {todayClasses[i]['name']} 
                    ministered by {todayClasses[i]['teacher']} at {i.split(':')[0]} hours and {i.split(':')[1]} minutes''',
                    200
                )
        weekDay += 1
        nowTime = datetime.strptime("0:00", "%H:%M").time()
    
    return Response("No classes found", 200)

@app.route("/nowClass")
def nowClass():
    nowDateTime = datetime.now()
    nowTime = nowDateTime.time()
    weekDay = nowDateTime.isoweekday()
    todayClasses = getDayClasses(weekDay) 
    for i in todayClasses:
        classTime = datetime.strptime(i, "%H:%M")
        classDuration = datetime.strptime(todayClasses[i]["duration"], "%H:%M").time()
        classEnd = classTime + timedelta(hours=classDuration.hour, minutes=classDuration.minute)

        if (nowTime <= classEnd.time() and nowTime > classTime.time()):
            timeRemaining = f"{str(classEnd.time().hour - nowTime.hour)} hours and {str(classEnd.time().minute - nowTime.minute)} minutes"
            return Response(f'''
                            You're currently in class, {todayClasses[i]["initials"]} {todayClasses[i]["name"]} ministered by {todayClasses[i]["teacher"]}, time remaining {timeRemaining}
                            ''', 200)
    return Response("You're not currently in class", 200)
    
@app.route("/smartQuestion", methods=["POST"])
def smartQuestions():
    nowDateTime = datetime.now()
    weekDay = nowDateTime.isoweekday()
    day: str = request.args.get("day").lower() 
    dayNumber:int = 0
    classOrder: str = request.args.get("order")
    print(f"day: {day}")
    print(f"classOrder: {classOrder}")
    
    # get the day number based on the input
    for i in days.keys():
        if (day == i):
            if (day == 'today'):
                dayNumber = weekDay
            elif (day == 'tomorrow'):
                dayNumber = weekDay + 1
            elif(day ==  "yesterday"):
                dayNumber = weekDay - 1
            else:
                dayNumber = days[i]

    dayClasses = getDayClasses(dayNumber)
    classesKeys = list(dayClasses)
    
    if (len(dayClasses) == 0):
        return Response("You don't have any classes in the choosen day", 200)
    
    if (classOrder == None):
        return Response(allDayClasses(dayClasses), 200)
    else:
        if(classOrder == "1st"):
            classOrderNumber = 0
        else:
            classOrderNumber =  len(classesKeys) - 1
        print(classOrderNumber)
        return Response(f''' Your {day}'s {classOrder} class is {dayClasses[classesKeys[classOrderNumber]]["initials"]} {dayClasses[classesKeys[classOrderNumber]]["name"]} 
                            ministered by {dayClasses[classesKeys[classOrderNumber]]["teacher"]} 
                            at {classesKeys[classOrderNumber].split(":")[0]} hours and {classesKeys[classOrderNumber].split(":")[1]} minutes 
                        ''',
                        200)
    
    
@app.route("/test")
def test():
    return Response("1", 200)    
    


app.run("192.168.15.190", debug=True, port=5070)