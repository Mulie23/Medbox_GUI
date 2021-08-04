import json
with open("container.json") as f:
    container_data = json.load(f)
for j in container_data:
    print(j)