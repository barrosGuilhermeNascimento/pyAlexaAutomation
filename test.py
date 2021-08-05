import requests
# file to run tests
from functions import trello

trello = trello.Trello("AlexaBoard")
print(trello.Board.lists[0].cards[0])