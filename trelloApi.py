import requests
import os
import dotenv
import json


dotenv.load_dotenv()

class Trello:
    def __init__(self):
        self.key = os.getenv("TRELLOKEY")
        self.token = os.getenv("TRELLOTOKEN")
        self.board = "v79CUYAD"
        
    def getCards(self):
        self.limit = '30'
        url = 'https://api.trello.com/1/boards/' + self.board + '/cards/?limit=' + self.limit + "&members_fields=fullName&key=" + self.key + '&token=' + self.token
        
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }

        call = requests.get(url , headers=headers)

        print(call.text)
    
    def getCheckListsFromCard(self):
        self.limit = '30'
        url = 'https://api.trello.com/1/boards/' + self.board + "/checklists?key=" + self.key + '&token=' + self.token
        
        headers = {
            'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        }
        call = requests.get(url , headers=headers)

        print(call.text)
        
        
instantClass = Trello()
instantClass.getCards()
instantClass.getCheckListsFromCard()