import json
with open("container.json") as f:
    container_data = json.load(f)
with open("prescription.json") as f:
    prescription_data = json.load(f)
prescription_list = prescription_data["data"]["prescription"]
print(prescription_list)
med_list=[]
for i in range(len(prescription_list)):
    med_list.append(prescription_list[i]["medicine_name"])
print(med_list)
# for i in med_list:
#     if  container_data.get(i) is None: