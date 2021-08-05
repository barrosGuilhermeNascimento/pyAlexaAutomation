from datetime import datetime, time, timedelta
from typing import List

from flask import Response, request
from models import universityModel

days: dict = {"monday":"1", "tuesday":"2", "wednesday": "3", "thursday": "4", "friday": "5", "saturday": "6", "sunday":"7", "tomorrow": "", "yesterday": "", "today": ""}


# Util functions
def getDayClasses(day: int, classFile: List[universityModel.DayClassesModel]):
    todayClasses: universityModel.DayClassesModel = classFile[str(day)]    
    return todayClasses

def allDayClasses(todayClasses: universityModel.DayClassesModel):
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


# Controller Functions
def nextClass( classFile: List[universityModel.DayClassesModel]):
    nowDateTime = datetime.now()
    nowTime = nowDateTime.time()
    weekDay = nowDateTime.isoweekday()
    todayClasses = getDayClasses(weekDay, classFile)
    while (weekDay < 6):
        todayClasses: dict = classFile[str(weekDay)]
        for i in todayClasses.keys():
            classTime = datetime.strptime(i, "%H:%M").time()
            if ( nowTime < classTime):
                return f'''Your next Class is: {todayClasses[i]['initials']} {todayClasses[i]['name']} 
                    ministered by {todayClasses[i]['teacher']} at {i.split(':')[0]} hours and {i.split(':')[1]} minutes''',
        weekDay += 1
        nowTime = datetime.strptime("0:00", "%H:%M").time()
    
    return "No classes found"

def currentClass(classFile: List[universityModel.DayClassesModel]):
    nowDateTime = datetime.now()
    nowTime = nowDateTime.time()
    weekDay = nowDateTime.isoweekday()
    todayClasses = getDayClasses(weekDay, classFile) 
    for i in todayClasses:
        classTime = datetime.strptime(i, "%H:%M")
        classDuration = datetime.strptime(todayClasses[i]["duration"], "%H:%M").time()
        classEnd = classTime + timedelta(hours=classDuration.hour, minutes=classDuration.minute)

        if (nowTime <= classEnd.time() and nowTime > classTime.time()):
            timeRemaining = f"{str(classEnd.time().hour - nowTime.hour)} hours and {str(classEnd.time().minute - nowTime.minute)} minutes"
            return f''' You're currently in class, {todayClasses[i]["initials"]} {todayClasses[i]["name"]} 
                        ministered by {todayClasses[i]["teacher"]}, time remaining {timeRemaining}
                    '''
    return "You're not currently in class"
    
    
def GetClassesDayOrder(args , classFile: List[universityModel.DayClassesModel]):
    nowDateTime = datetime.now()
    weekDay = nowDateTime.isoweekday()
    day: str = args.get("day").lower() 
    dayNumber:int = 0
    classOrder: str = args.get("order")
    
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
        return "You don't have any classes in the choosen day"
    
    if (classOrder == None):
        return allDayClasses(dayClasses)
    else:
        if(classOrder == "1st"):
            classOrderNumber = 0
        else:
            classOrderNumber =  len(classesKeys) - 1
        return f''' Your {day}'s {classOrder} class is {dayClasses[classesKeys[classOrderNumber]]["initials"]} {dayClasses[classesKeys[classOrderNumber]]["name"]} 
                    ministered by {dayClasses[classesKeys[classOrderNumber]]["teacher"]} 
                    at {classesKeys[classOrderNumber].split(":")[0]} hours and {classesKeys[classOrderNumber].split(":")[1]} minutes 
                '''

