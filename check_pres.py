import requests 
import json

header = {"jwt" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiaWF0IjoxNjI3NDU1MzM4LCJleHAiOjE2Mjc1NDE3Mzh9.YPddmGSFu-M0RD-_x5zQHdVOW2JLSVPP_2oAhxLGehk"}
body = {"medboxID": "1","username": "user1"}

response3 = requests.post("http://3.0.17.207:4000/queue/consume", body, headers=header)
data = response3.json()
with open ("prescription.json","w") as f:
    json.dump(data,f)
print(data)