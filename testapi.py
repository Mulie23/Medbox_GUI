import requests 
import json
import base64

login = 'FN.LN@your_email.com'
password = 'your_PW'
response = requests.get('your_JSON_URL', auth=(login, password))
data = response.json()
with open('data.json', 'w') as f:
    json.dump(data, f)
print(data)