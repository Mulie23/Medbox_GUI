import json
with open("D:/Term 8/Capstone/guizero/Medbox_GUI/prescription.json") as f:
    data1 = json.load(f)
print(data1["data"]["prescription"][0]["time"]["tuesday"])