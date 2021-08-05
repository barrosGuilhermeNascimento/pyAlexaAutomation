from typing import List
import requests
import os
import dotenv
import json
from models import trelloModel


dotenv.load_dotenv()

class Trello:
    
    Board: trelloModel.BoardModel = trelloModel.BoardModel()

    #region Configurations
    def __init__(self, boardName):
        self.__key = os.getenv("TRELLOKEY")
        self.__token = os.getenv("TRELLOTOKEN")        
        self.__baseUrl = "Https://api.trello.com"
        self.__headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        self.boardId = self.getBoardId( boardName)
        self.syncBoardData()
        
    # def __getattribute__(self, item: str):
    #     if (item.startswith('_') or callable(vars(Trello)[item])):
    #         return super(Trello, self).__getattribute__(item)
    #     if ('sync' + item.lower().capitalize() in [p[0] for p in vars(Trello).items() if callable(p[1])]):
    #         exec('self.sync{}Data()'.format(item.lower().capitalize()))
    #     return super(Trello, self).__getattribute__(item)
    #endregion

    ## Getting data     
    def syncCheckListData(self, cardId: List[str]):
        checkListArray: List[trelloModel.CheckListModel] = [] 
        for i in cardId:
            checkListDataUrl = f'{self.__baseUrl}/1/checklists/{i}/?key={self.__key}&token={self.__token}'
            reqResponse = requests.get(checkListDataUrl, headers=self.__headers).json()
            checkListObj = trelloModel.CheckListModel()
            checkListObj.checkListId = reqResponse["id"]
            checkListObj.name = reqResponse["name"]
            checkListObj.itens = []
            for x in reqResponse["checkItems"]:
                checkItemObj = trelloModel.CheckListItemModel()
                checkItemObj.id = x["id"]
                checkItemObj.name = x["name"]
                checkItemObj.due = x["due"]
                checkItemObj.checked = x["state"] == 'complete' if True else False
                checkListObj.itens.append(checkItemObj)
            checkListArray.append(checkListObj)
        return checkListArray
       
    def syncCardsData(self, listId):
        cardDataUrl = f'{self.__baseUrl}/1/lists/{listId}/cards/?key={self.__key}&token={self.__token}'
        reqResponse = requests.get(cardDataUrl, headers=self.__headers)
        trelloCardsList: List[trelloModel.CardModel] = []
        for i in reqResponse.json():
            trelloCardObj = trelloModel.CardModel()
            trelloCardObj.listid = i["idList"]
            trelloCardObj.cardId = i["id"]
            trelloCardObj.name = i["name"]
            trelloCardObj.desc = i["desc"]
            trelloCardObj.dueDate = i["due"]
            trelloCardObj.dueComplete = i["dueComplete"]                
            trelloCardObj.checklists = self.syncCheckListData(i["idChecklists"])
            trelloCardsList.append(trelloCardObj)
        return trelloCardsList
            
    
    def syncListsData(self):
        getListsIdsUrl = f'{self.__baseUrl}/1/boards/{self.boardId}/lists/?key={self.__key}&token={self.__token}'
        listsIdResponse = requests.get(getListsIdsUrl, headers=self.__headers)
        trelloListArray: List[trelloModel.ListsModel] = []
        for i in listsIdResponse.json():
            trelloListObj = trelloModel.ListsModel()
            trelloListObj.listId = i["id"]
            trelloListObj.name = i["name"]
            trelloListObj.idBoard = i["idBoard"]
            trelloListObj.cards = self.syncCardsData(i["id"])
            trelloListArray.append(trelloListObj)
        return trelloListArray

        
    def syncBoardData(self) -> None:
        getBoardUrl = f'{self.__baseUrl}/1/boards/{self.boardId}/?key={self.__key}&token={self.__token}'
        
        reqResponse = requests.get(getBoardUrl , headers=self.__headers)
        self.Board.boardId = reqResponse.json()["id"]
        self.Board.name = reqResponse.json()["name"]
        self.Board.labels = trelloModel.LabelsModel.fromJson(reqResponse.json()["labelNames"])
        funcReturn = self.syncListsData()
        self.Board.lists = funcReturn
        
    def getBoardId(self, boardName: str) -> int:
        getBoardIdUrl = f'{self.__baseUrl}/1/members/me/boards/?key={self.__key}&token={self.__token}'
        reqResponse = requests.get(getBoardIdUrl, headers=self.__headers)
        for i in reqResponse.json():
            if (i["name"].lower() == boardName.lower()):
                return i["shortLink"]
            
        raise ValueError('The board was not found')