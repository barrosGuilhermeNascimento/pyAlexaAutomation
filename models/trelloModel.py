from typing import List, TypedDict, Union
from datetime import datetime
import json

class LabelsModel():
    
    def __init__(self, *args, **kwargs) -> None:
        for i in kwargs.keys():
            exec(f'self.{i} = kwargs["{i}"]')
    
    @classmethod
    def fromJson(cls, jsonInput):
        if (type(jsonInput) == str):
            return cls(**json.loads(jsonInput))
        elif (type(jsonInput) == dict):
            return cls(**jsonInput)
            
    
class CheckListItemModel:
    id: str
    name: str    
    dueDate: Union[datetime, None]
    checked: bool = False

class CheckListModel:
    checkListId: str
    name: str
    itens: List[CheckListItemModel]

class CardModel:
    cardId: str
    name: str
    desc: str
    listid: str
    dueDate: Union[datetime, None]
    checklists: List[CheckListModel]
    
    def __init__(self):
        self.closed: bool = False
        self.dueComplete: bool = False
        
    def __str__(self) -> str:
        return '{"cardId":%s, "name": %s, "desc": %s, "listid": %s, "dueDate": %s}' % (self.cardId, self.name, self.desc, self.listid, self.dueDate)

class ListsModel:
    listId: str
    name: str 
    idBoard: str
    cards: List[CardModel]
    
    def __init__(self):
        self.closed: bool = False

class BoardModel():
    boardId: str
    name: str
    labels: LabelsModel
    lists: List[ListsModel] = [ListsModel()]
        
        