from typing import List

class ClassModel:
    initials: str
    name: str
    teacher: str
    duration: str
    
class ClassObjectModel:
    time: ClassModel
    
class DayClassesModel:
    dayNumber: List[ClassModel]