import requests 

header = {"jwt" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiaWF0IjoxNjI2ODQyNjY1LCJleHAiOjE2MjY5MjkwNjV9.L_bOISzaIMUGM9d0L0dbGjFQt_tHmf4ZQ1Rl-Lo1GDY"}
body = {"medboxID": "1","username": "user1"}

response3 = requests.post("http://3.0.17.207:4000/queue/consume", body, headers=header)
data = response3.json()
print(data)