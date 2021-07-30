import json
with open("prescription.json") as f:
    data = json.load(f)
for i in data["data"]["prescription"]:
    print(i)

