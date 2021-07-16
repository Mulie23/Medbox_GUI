import requests 

header = {"jwt" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiaWF0IjoxNjI2NDA0OTAxLCJleHAiOjE2MjY0OTEzMDF9.mj-K-OZij9k_fRzt0GWvvyTrt95ygvzMnKKjAD7FYgY"}
body = {"medboxID": "1","username": "user1"}

response3 = requests.post("http://3.0.17.207:4000/notification/send", body, headers=header)
data = response3.json()
print(data)
