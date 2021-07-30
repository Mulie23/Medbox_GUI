import json
class Containers() : 
    def __init__(self, DIR, STEP, SLEEP) : 
        self.DIR = DIR
        self.STEP = STEP
        self.SLEEP = SLEEP
        self.data = None 
        self.filled_containers = {}
        self.unfilled_containers = [] 
        self.current_pos = None 
        self.extractContainerData() 
    
    def extractContainerData(self) : 
        f  = open('container.json')
        self.data = json.load(f)
        self.current_pos = self.data["current_pos"]
        for i in self.data:
            if i!="current_pos" : 
                if self.data[i]["filled"]==1 : 
                    self.filled_containers[self.data[i]["medicine"]["id"]] = i
                else : 
                    self.unfilled_containers.append(i) 
        f.close() 

    def getContainer(self, medicineID ) : 
        # if container exists get id, else allocate and return id 
        # if no free container return None 
        if medicineID in self.filled_containers.keys() : 
            print(self.filled_containers)
            return self.filled_containers[medicineID]
        else : 
            if len(self.unfilled_containers)==0 : 
                return None 
            else : 
                with open("prescription.json") as f:
                    data = json.load(f)
                for i in data["data"]["prescription"]:
                    if i["medicine_id"] == medicineID:
                        medicine_name_in_pres = i["medicine_name"]
                        message_in_pres = i["message"]
                refilling_quantity.value=medicine_name_in_pres
                print(refilling_quantity.value)
                container_id  = self.unfilled_containers.pop(0) 
                self.data[container_id]["filled"] = 1 
                self.data[container_id]["quantity_left"] = 0 
                self.data[container_id]["medicine"] = {
                    "id": medicineID,
                    "name": medicine_name_in_pres, # need to retrive somehow from db ? 
                    "message": message_in_pres # need to retrive from db ? 
                }
                self.filled_containers[medicineID] = container_id
                return container_id
    
    def calc_turn_angle(self, current, destination):
        CW = 1
        CCW = 0
        ang = destination - current
        if 0 <= ang <= 6:
            return (30*ang),CW
        elif 7 <= ang <= 11:
            ang = 12-ang
            return (30*ang),CCW
        elif -11 <= ang <= -7:
            ang = 12 + ang
            return (30*ang),CW
        elif -6 <= ang <=-1:
            ang = (-1)*ang
            return (30*ang),CCW

    def turn_stepper(self, deg, direction):
        SPR = 200
        delay = 1.2/SPR
        self.DIR.on() if direction == 1 else self.DIR.off()
        steps = int(SPR*deg/360)
        self.SLEEP.on()
        sleep(0.5)
        for x in range(steps):
            self.STEP.on()
            sleep(delay)
            self.STEP.off()
            sleep(delay)
        sleep(0.5)
        self.SLEEP.off()
        print('turnt')

    def updateContainerInformation(self, container_id, number_of_pills) : 
        # update infromation in the container.json file
        self.data[container_id]["quantity_left"] += number_of_pills 

    def rotateContainerToRefillArea(self,container_id) : 
        offset = 2
        ids = int(container_id[-1])
        current = int(self.data['current_pos'])  #current container at the refill spot
        destination = ids - offset
        if destination <= 0 :
            destination = 12 - destination
        else:
            None
        if current != destination:
            ang, dire = self.calc_turn_angle(current, destination)
            print(ang, dire)
            self.turn_stepper(ang, dire)
            self.data['current_pos'] = destination
            self.current_pos = destination
        else:
            None
        # return true upon success and false upon failure 
        return True 
        

    def rotateContainerToDispenseArea(self, container_id) : 
        ids = int(container_id[-1])
        current = int(self.data['current_pos'])
        destination = ids
        if current != destination:
            ang, dire = self.calc_turn_angle(current, destination)
            print(ang, dire)
            self.turn_stepper(ang, dire)
            self.data['current_pos'] = destination
            self.current_pos = destination
        else:
            None
        # return true upon success and false upon failure 
        return True 
    
    
    def writeToFile(self) : 
        with open("container.json", 'w') as outfile:
            json.dump(self.data, outfile)


container = Containers(DIR, STEP, SLEEP) 
container_id = container.getContainer("101")
print(container_id)