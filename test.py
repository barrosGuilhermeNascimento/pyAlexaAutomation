import requests
from requests.api import head

request = requests.post('http://192.168.15.190:5070/smartQuestion', json={"test":"test"}, headers={'Accept': 'application/json'})
print(dir(request))