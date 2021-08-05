
from typing import List, TypedDict, Union
from datetime import datetime

class labels(TypedDict):
    green: str
    yellow: str
    orange: str
    red: str
    purple: str
    blue: str
    sky: str
    lime: str
    pink: str
    black: str
    
class CheckListItemModel:
    id: str
    name: str    
    dueDate: Union[datetime, None]
    state: bool = False

class CheckListModel:
    id: str
    name: str
    itens: List[CheckListItemModel]

class CardModel:
    id: str
    name: str
    desc: str
    dueDate: Union[datetime, None]
    checklists: List[CheckListModel]
    
    def __init__(self):
        self.closed: bool = False
        self.dueComplete: bool = False

class ListsModel:
    id: str
    name: str 
    idBoard: str
    cards: List[CardModel]
    
    def __init__(self):
        self.closed: bool = False

class BoardModel:
    id: str
    name: str
    lastModified: datetime
    labels: labels
    lists: List[ListsModel]
        
        