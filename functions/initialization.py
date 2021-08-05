import json
from models import universityModel
from typing import List


def Init():
    file = open("./classes.json")
    classFile: List[universityModel.DayClassesModel] = json.load(file)
    file.close()
    return classFile