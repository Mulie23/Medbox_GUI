import requests 

header = {"jwt" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiaWF0IjoxNjI2MjMzNDAyLCJleHAiOjE2MjYzMTk4MDJ9._HjrM5XbmKZbMATpCZ2_1w3hbWpfQm2-svLTOxW7AAE"}
body = {"medboxID": "1","username": "user1"}

response3 = requests.post("http://3.0.17.207:4000/queue/consume", body, headers=header)
data = response3.json()
print(data)

