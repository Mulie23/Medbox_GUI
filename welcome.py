from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window, info, Box
import requests 
import json
import base64
import random
import string
import os.path
import datetime
import threading
from playsound import playsound
import subprocess
import os
timer=0
timer_1=0
timer_2=0
timer_3=0
"""
NOTE : for the program to work , you need to have network-manager installed in the linux machine
TODO : to install network-manager run - 
     sudo apt install network-manager 

"""

def check_ping():
    hostname = "google.com"
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        return True
    else:
        return False

class WIFI : 
    def __init__(self) :
        pass
        


    def scan_windows(self) : 
        self.dictData = {} 
        #devices = subprocess.check_output(['wlan','network'])
        # decode it to strings
        devices = devices.decode('ascii')
        devices= devices.replace("\r","")
        devices = devices.split("\n\n")

        for i in devices[1:-1] : 
            temp = i.split("\n")
            name = temp[0].split(":")[-1].strip(" ")
            interface = temp[2].split(":")[-1].strip(" ")
            self.dictData[name] = interface 
    
    """
    @arguments
        name is from the data 
        password is from the GUI
        interface wifi.data[name]

    """
    
    def scan(self) :
        devices = os.popen("nmcli device wifi list").read()
        devices.replace("\r", " ")
        devices = devices.split("\n")
        data = set() 
        for i in devices[1:-1] :
            temp = i.split("\n")
            name = temp[0].replace("  "," ").split(" ")[4]
            data.add(name)
        return list(data)
           
        
    
    def connect(self, name, password = None, interface=None) : 
        try:
            base = "nmcli d wifi connect {}".format(name)
            if password!=None :
                base += " password {}".format(password)
            if interface!=None :
                base += " iface {}".format(interface)
            os.system(base) 
        except:
            raise
        else:
            return True

wifi = WIFI()
# wifi = WIFI()
# print(wifi.scan())
# print(wifi.connect("WT", "15168877330"))

from time import sleep
import gpiozero as gpio
import RPi.GPIO as GPIO
import pigpio
import json
import serial
import pygame
pygame.init()
pygame.mixer.music.load('/home/pi/Documents/Medbox_GUI/samsung_alarm.mp3')

os.system('sudo pigpiod')

GPIO.setmode(GPIO.BCM)
pi = pigpio.pi()
pi.set_servo_pulsewidth(17,1970)
pi.set_servo_pulsewidth(24,1500)
sleep(2)
pi.set_servo_pulsewidth(17,0)
pi.set_servo_pulsewidth(24,0)

# setup all pins
#stepper motor
DIR = gpio.OutputDevice(21)
STEP = gpio.OutputDevice(20)
SLEEP = gpio.OutputDevice(26)
CW = 1
CCW = 0
SPR = 200
SLEEP.off() #puts the board in sleep mode
DIR.on() #sets to clockwise
delay = 2.4/SPR

# setup pump pins
VALVE = gpio.OutputDevice(13)
PUMP = gpio.OutputDevice(19)
DIST = gpio.InputDevice(23) #0 means that smth is close
NDIST = gpio.InputDevice(22) #0 means that smth is close
VALVE.off()
PUMP.off()

# setup scanner pins
SCANNER = gpio.OutputDevice(4)
SCAN = gpio.OutputDevice(27)

# setup current sensor pins and variables
import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)


def play_alarm():
    pygame.mixer.music.play()
    # sounds alarm 
    return True

def stop_alarm():
    pygame.mixer.music.stop()
    return True

def turn_servo(pos):
    pi = pigpio.pi()
    pi.set_pull_up_down(24, pigpio.PUD_DOWN)
#     pi.set_PWM_frequency(24, 50)
    servo = "180"
    if servo == "180":
        default = 1500
        dispense = 875
        if pos == "dispense":
            for i in range (default-200, dispense-1, -25):
                pi.set_servo_pulsewidth(24, i)
                sleep(0.2)
            sleep(1)
            pi.set_servo_pulsewidth(24, 0)
        elif pos == "default":
            pi.set_servo_pulsewidth(24, default)
    elif servo == "continuous":
        pos_dict = {"default": 1580, "dispense": 1400}
        pi.set_servo_pulsewidth(24,pos_dict[pos])    
        sleep(0.9)
        pi.set_servo_pulsewidth(24,0)
    return True



def lower_nozzle():
    pi = pigpio.pi()
    pi.set_pull_up_down(17, pigpio.PUD_DOWN)
    max_height = 1970
    pi.set_servo_pulsewidth(17,max_height)
#     cutoff = 12350
    PUMP.on()
    VALVE.off()
    sleep(1)
    cutoff = chan.value + 60
    pi.set_servo_pulsewidth(17,1300)
    try:
        for i in range(max_height, 1029, -100):
            pi.set_servo_pulsewidth(17, i)
            sleep(0.5)
            print(chan.value, cutoff)
            if NDIST.value == 0:
                for j in range(i-50, 1019, -5):
                    pi.set_servo_pulsewidth(17, j)
                    sleep(0.5)
                    print(chan.value, cutoff)
                    if chan.value >= cutoff:
                        pi.set_servo_pulsewidth(17, max_height)
                        sleep(3)
                        pi.set_servo_pulsewidth(17, 0)
                        print("pill picked up")
                        break
                sleep(1)
                break
        
    except KeyboardInterrupt:
        pi.set_servo_pulsewidth(17, max_height)
        pi.set_servo_pulsewidth(17, 0)
#         PUMP.off()
        sleep(4)
        print('interrupted')
        
    pi.set_servo_pulsewidth(17, max_height)
    sleep(3)
    pi.set_servo_pulsewidth(17, 0)
    return True

def dispense(med_id, qty):
    qty_left = qty
    container = Containers(DIR, STEP, SLEEP)
    container_id = container.getContainer(med_id)
    container.rotateContainerToDispenseArea(container_id)
    while qty_left != 0:
        lower_nozzle() #turns on pump and lowers vacuum nozzle, the nozzle will rise after getting clsoe to a pill
        turn_servo("dispense")#moves nozzle over the dispensing area
        VALVE.on()
        sleep(1)
        PUMP.off()
        VALVE.off()
        sleep(0.5)
        turn_servo("default")
        qty_left = qty_left - 1
    container.updateContainerInformation(container_id, -qty)
    container.writeToFile()    
    return True

def refillProcess() : 
    # pull updated prescription 
    container = Containers(DIR, STEP, SLEEP) 
    stateMachine = True ; 
    state = 'barcode'
    while(stateMachine) : 
        if (state=="barcode") : 
            quantity_window.show(wait=True)
            refill_window.hide()
            #display the relevant details on the front end - Wentao
            # information on what medicine are to be filled up 
            medicine_id = checkBarcode() ; 
            if medicine_id!=None : 
                state = "rotate"

            # add GUI interrupt 
        elif (state=="rotate") : 
            container_id = container.getContainer(medicine_id)
            if container.rotateContainerToRefillArea(container_id) : 
                state="finish"
            else : 
                state = "error"
                message = "couldn't rotate container"
        # elif (state=="wait") : 
        #     # wait for a button push on gui and number of pills form input 
        #     # update infromation i.e container.json
        #     if refillComplete() : 
        #         state = "finish"
        #     else : 
        #         state = "barcode" 
        elif (state=="finish"): 
            container.writeToFile() 
            stateMachine = False 
#            refill_window.show(wait=True)
        elif  (state=="error") : 
            error = "there was some error" 
            stateMachine = False 
        else : 
            state = "error" 
            error = "invalid sate" 
    return  True

def refillComplete() : 
    # return true if all the medicines have been refilled 
    # return false if more medicines have to be filled
    return 


def checkBarcode() :
    # turn on scanner and reads te barcode. returns a 5 digit id
    ser = serial.Serial("/dev/ttyS0", 115200, timeout=0.5)
    SCANNER.on()
    SCAN.off() #button not pressed
    info = b''
    sleep(1)
    while info == b'':
        print('scanning')
        SCAN.on()
        counter = 0
        while info == b'' and counter <= 4:
            info = ser.readline()
            sleep(1)
            counter += 1
        SCAN.off()
        sleep(1)
    f = open('med_id.json')
    med_id_check = json.load(f)
    info = str(tuple(list(info)))
    print(info)
    SCANNER.off()
    for i in med_id_check:
        if i == info:
            return med_id_check[i]["id"]
        else:
            None
    return None 
    


def pullPrescription() : 
    # if prescription is updated 
        # update the prescription 
    return True 


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
            container_id = self.filled_containers[medicineID]
            refilling_quantity.value = self.data[container_id]["medicine"]["name"]
            return container_id
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
            destination = 12 + destination
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
        with open("/home/pi/Documents/Medbox_GUI/container.json", 'w') as outfile:
            json.dump(self.data, outfile)
# container = Containers(DIR, STEP, SLEEP)
# import os
# os.system('sudo killall pigpiod')
# os.system('sudo pigpiod')
# container.rotateContainerToDispenseArea("container_6")
# dispense(59,1)

# turn_servo("dispense")
# sleep(2)
# turn_servo("default")


def finish_yes_func():
    global isfinish
    global yesno_press
    yesno_press = True
    isfinish = True
    confirm_finish_window.hide()
    menu_window.show(wait=True)

def finish_no_func():
    global isfinish
    global yesno_press
    yesno_press = True
    isfinish = False
    confirm_finish_window.hide()


def add_one():
    int_qun = int(quantity_no.value)
    int_qun += 1
    quantity_no.value =int_qun

def add_five():
    int_qun = int(quantity_no.value)
    int_qun += 5
    quantity_no.value =int_qun

def add_ten():
    int_qun = int(quantity_no.value)
    int_qun += 10
    quantity_no.value =int_qun

def minus_one():
    int_qun = int(quantity_no.value)
    int_qun -= 1
    quantity_no.value =int_qun

def minus_five():
    int_qun = int(quantity_no.value)
    int_qun -= 5
    quantity_no.value =int_qun

def minus_ten():
    int_qun = int(quantity_no.value)
    int_qun -= 10
    quantity_no.value =int_qun

def submit_quan():
    global submit_quan
    submit_quan = True
    quantity_window.hide()
    scan_window.hide()

def check_submit_quan():
    global submit_quan_value
    while submit_quan_value == False:
        quantity_window.show(wait=True)
    return True

def refill_notification():
    playsound('noti1.wav')
    refill_window.info("Notificaiton", "Please refill medicines first")
    refill_window.show(wait=True)

def compare():
    with open("/home/pi/Documents/Medbox_GUI/container.json") as f:
        container_data = json.load(f)
    with open("prescription.json") as f:
        prescription_data = json.load(f)
    prescription_list = prescription_data["data"]["prescription"]
    # print(prescription_list)
    med_list=[]
    for i in range(len(prescription_list)):
        med_list.append(prescription_list[i]["medicine_name"])
    # print(med_list)
    for i in med_list:
        if  container_data.get(i) is None:
            timer1 = threading.Timer(900, dispense1)
            timer.start()
            refill_notification()
            return
    #show medicine names
    dispense_window.show(wait=True)
    dispense_all()
     
def dispense_all():
    global timer_1
    global timer_2
    dispense_window.show(wait=True)
    with open("/home/pi/Documents/Medbox_GUI/container.json") as f:
        container_data = json.load(f)
    with open("prescription.json") as f:
        prescription_data = json.load(f)
    week_list=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]     
    day_int = datetime.datetime.today().weekday()
    day_str = week_list[day_int]
    now_session = 0
    now = datetime.datetime.now()
    today10am = now.replace(hour=10, minute=0, second=0, microsecond=0)
    today1pm = now.replace(hour=13, minute=0, second=0, microsecond=0)
    today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)
    if now < today10am:
        now_session = 0
    elif now < today1pm:
        now_session = 1
    elif now < today5pm:
        now_session = 2
    else:
        now_session = 3
    n = 0
    for i in prescription_data["data"]["prescription"]:
        med_name_to_dispense = i["medicine_name"]
        med_id_to_dispense = i["medicine_id"]
        med_quantity_to_dispense = i["time"][day_str][now_session]
        if med_quantity_to_dispense != 0:
            dispense(med_id_to_dispense,med_quantity_to_dispense)
            for j in container_data:
                if j != "current_pos":
                    if container_data[j]["medicine"]["id"] == med_id_to_dispense:
                        container_data[j]["quantity_left"] -= med_quantity_to_dispense
            n += 1
            if n == 1:
                medicine_name1_dis.value = med_name_to_dispense
                medicine_quantity1_dis.value = med_quantity_to_dispense
            if n == 2:
                medicine_name2_dis.value = med_name_to_dispense
                medicine_quantity2_dis.value = med_quantity_to_dispense        
            if n == 3:
                medicine_name3_dis.value = med_name_to_dispense
                medicine_quantity3_dis.value = med_quantity_to_dispense     
            if n == 4:
                medicine_name4_dis.value = med_name_to_dispense
                medicine_quantity4_dis.value = med_quantity_to_dispense     
            if n == 5:
                medicine_name5_dis.value = med_name_to_dispense
                medicine_quantity5_dis.value = med_quantity_to_dispense     
            if n == 6:
                medicine_name6_dis.value = med_name_to_dispense
                medicine_quantity6_dis.value = med_quantity_to_dispense     
            if n == 7:
                medicine_name7_dis.value = med_name_to_dispense
                medicine_quantity7_dis.value = med_quantity_to_dispense     
            if n == 8:
                medicine_name8_dis.value = med_name_to_dispense
                medicine_quantity8_dis.value = med_quantity_to_dispense     
            if n == 9:
                medicine_name9_dis.value = med_name_to_dispense
                medicine_quantity9_dis.value = med_quantity_to_dispense     
            if n == 10:
                medicine_name10_dis.value = med_name_to_dispense
                medicine_quantity10_dis.value = med_quantity_to_dispense     
            if n == 11:
                medicine_name11_dis.value = med_name_to_dispense
                medicine_quantity11_dis.value = med_quantity_to_dispense     
            if n == 12:
                medicine_name12_dis.value = med_name_to_dispense
                medicine_quantity12_dis.value = med_quantity_to_dispense    
    with open("/home/pi/Documents/Medbox_GUI/container.json","w") as f:
        json.dump(container_data, f)                  
    play_alarm()
    timer_1 = threading.Timer(60, play_alarm)
    timer_1.start()   
    timer_2 = threading.Timer(120, notificate)
    timer_2.start()   
    set_timer()


random_code = ""

def confirm_finish():
    with open("/home/pi/Documents/Medbox_GUI/container.json") as f:
        data = json.load(f)
    for i in data:
        if i != "current_pos":
        # print(data[i]["medicine"]["name"])
        # print(refilling_quantity.value)
            if data[i]["medicine"]["name"] == refilling_quantity.value:
                data[i]["quantity_left"] += int(quantity_no.value)
    with open("/home/pi/Documents/Medbox_GUI/container.json","w") as f:
        json.dump(data, f)
    medicine_info_check()
    refill_window.show(wait=True)

def notificate():
    with open("/home/pi/Documents/Medbox_GUI/data.json") as f:
        data = json.load(f)
    header = {"jwt":data["data"]["jwt"]}
    # header = {"jwt" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiaWF0IjoxNjI2ODQyNjY1LCJleHAiOjE2MjY5MjkwNjV9.L_bOISzaIMUGM9d0L0dbGjFQt_tHmf4ZQ1Rl-Lo1GDY"}
    with open("/home/pi/Documents/Medbox_GUI/pass.json") as f:
        data = json.load(f)    
    body = {"username":data["username"],"medboxID":"1"}
    response = requests.post("http://3.0.17.207:4000/notification/send", body, headers=header)
    data = response.json()
    with open("notification.json", "w") as f:
        json.dump(data, f)

def pull_pres():
    with open("/home/pi/Documents/Medbox_GUI/data.json") as f:
        data = json.load(f)
    header = {"jwt":data["data"]["jwt"]}
    with open("/home/pi/Documents/Medbox_GUI/pass.json") as f:
        data = json.load(f)    
    body = {"username":data["username"],"medboxID":"1"}
    # header = {"jwt" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiaWF0IjoxNjI2ODQyNjY1LCJleHAiOjE2MjY5MjkwNjV9.L_bOISzaIMUGM9d0L0dbGjFQt_tHmf4ZQ1Rl-Lo1GDY"}
    # body = {"medboxID": "1","username": "user1"}

    # response = requests.post("http://3.0.17.207:4000/queue/consume", body, headers=header)
    # data = response.json()
    # with open("prescription.json", "w") as f:
    #     json.dump(data, f)
    with open("/home/pi/Documents/Medbox_GUI/prescription.json") as f:
        data = json.load(f)
    week_list=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]     
    day_int = datetime.datetime.today().weekday()
    day_str = week_list[day_int]
    if len(data["data"]["prescription"]) >= 1:
        medicine_name1_chepre.value = data["data"]["prescription"][0]["medicine_name"]
        medicine_dose1_chepre.value = data["data"]["prescription"][0]["time"][day_str]
        medicine_message1_chepre.value = data["data"]["prescription"][0]["message"]
    if len(data["data"]["prescription"]) >= 2:
        medicine_name2_chepre.value = data["data"]["prescription"][1]["medicine_name"]
        medicine_dose2_chepre.value = data["data"]["prescription"][1]["time"][day_str]
        medicine_message2_chepre.value = data["data"]["prescription"][1]["message"]
    if len(data["data"]["prescription"]) >= 3:
        medicine_name3_chepre.value = data["data"]["prescription"][2]["medicine_name"]
        medicine_dose3_chepre.value = data["data"]["prescription"][2]["time"][day_str]
        medicine_message3_chepre.value = data["data"]["prescription"][2]["message"]
    if len(data["data"]["prescription"]) >= 4:
        medicine_name4_chepre.value = data["data"]["prescription"][3]["medicine_name"]
        medicine_dose4_chepre.value = data["data"]["prescription"][3]["time"][day_str]
        medicine_message4_chepre.value = data["data"]["prescription"][3]["message"]
    if len(data["data"]["prescription"]) >= 5:
        medicine_name5_chepre.value = data["data"]["prescription"][4]["medicine_name"]
        medicine_dose5_chepre.value = data["data"]["prescription"][4]["time"][day_str]
        medicine_message5_chepre.value = data["data"]["prescription"][4]["message"]
    if len(data["data"]["prescription"]) >= 6:
        medicine_name6_chepre.value = data["data"]["prescription"][5]["medicine_name"]
        medicine_dose6_chepre.value = data["data"]["prescription"][5]["time"][day_str]
        medicine_message6_chepre.value = data["data"]["prescription"][5]["message"]
    if len(data["data"]["prescription"]) >= 7:
        medicine_name7_chepre.value = data["data"]["prescription"][6]["medicine_name"]
        medicine_dose7_chepre.value = data["data"]["prescription"][6]["time"][day_str]
        medicine_message7_chepre.value = data["data"]["prescription"][6]["message"]
    if len(data["data"]["prescription"]) >= 8:
        medicine_name8_chepre.value = data["data"]["prescription"][7]["medicine_name"]
        medicine_dose8_chepre.value = data["data"]["prescription"][7]["time"][day_str]
        medicine_message8_chepre.value = data["data"]["prescription"][7]["message"]
    if len(data["data"]["prescription"]) >= 9:
        medicine_name9_chepre.value = data["data"]["prescription"][8]["medicine_name"]
        medicine_dose9_chepre.value = data["data"]["prescription"][8]["time"][day_str]
        medicine_message9_chepre.value = data["data"]["prescription"][8]["message"]
    if len(data["data"]["prescription"]) >= 19:
        medicine_name10_chepre.value = data["data"]["prescription"][9]["medicine_name"]
        medicine_dose10_chepre.value = data["data"]["prescription"][9]["time"][day_str]
        medicine_message10_chepre.value = data["data"]["prescription"][9]["message"]
    if len(data["data"]["prescription"]) >= 11:
        medicine_name11_chepre.value = data["data"]["prescription"][10]["medicine_name"]
        medicine_dose11_chepre.value = data["data"]["prescription"][10]["time"][day_str]
        medicine_message11_chepre.value = data["data"]["prescription"][10]["message"]
    if len(data["data"]["prescription"]) >= 12:
        medicine_name12_chepre.value = data["data"]["prescription"][11]["medicine_name"]
        medicine_dose12_chepre.value = data["data"]["prescription"][11]["time"][day_str]
        medicine_message12_chepre.value = data["data"]["prescription"][11]["message"]



def dispense1():
    pull_pres()
    compare()


def pm_to_am(time_string):
    if time_string[-2]=="A":
        time_string = time_string[:-2]
        hour_minute=time_string.split(":")
        if len(hour_minute[0]) == 1:
            hour_minute[0] = "0" + hour_minute[0]
        return hour_minute
    else:
        time_string = time_string[:-2]
        hour_minute=time_string.split(":")
        hour_int = int(hour_minute[0])+12
        hour_minute = [str(hour_int),hour_minute[1]]
        return hour_minute

def get_started():
    # global timer_3
    global wifi
    wifi = WIFI()
    if check_ping() == True:
        decide_screen()
    else:
        wifi_window.show(wait=True)
    # timer_3 = threading.Timer(15, dispense_all)
    # timer_3.start()
        
def decide_screen():
    file_exists = os.path.isfile("data.json") 
    # print(file_exists)
    if file_exists:
        # f = open("data.json", "r")
        # if f.read() == "":
        #     login_window.show(wait=True)
        #     f.close
        # else:
        with open("/home/pi/Documents/Medbox_GUI/data.json") as f:
            data = json.load(f)
        if data["success"]==1:
            menu_window.show(wait=True)
            menu_window.set_full_screen()
        else:
            login_window.show(wait=True)
    else:
        # f = open("data.json", "w")
        # f.write("")
        # f.close
        login_window.show(wait=True)




def back_window_login():
    login_window.hide()

def submit():
    body =  {"username": my_name.value , "password" : my_password.value }
    # print(body)
    with open("pass.json", "w") as f:
        json.dump(body, f)
    # body =  {"username": my_name.value , "password" : my_password.value }
    # print(body)
    response = requests.post("http://3.0.17.207:4000/medboxAuth/login", body)
    data = response.json()
    with open("data.json", "w") as f:
        json.dump(data, f)
    # print(data)
    if data["success"] == 1:
        setting_window.show(wait=True)
    elif data["success"] == 0:
        if data["error"] == "db connection error":
            login_window.info("Error", "Cannot connect to the database")
        elif data["error"] == "no such user exists":
            login_window.info("Error", "This is not a valid account")
        elif data["error"] == "username and passowrd did not match":
            login_window.info("Error", "Username and passowrd do not match")

def add_med():
    pass

def open_window1():
    add_med_window.show(wait=True)

def back_window1():
    add_med_window.hide()

def open_window2():
    quit_med_window.show(wait=True)

def back_window2():
    quit_med_window.hide()

def open_window3():
    pull_pres()
    check_pre_window.show(wait=True)

def back_window3():
    check_pre_window.hide()

def open_window4():
    medicine_info_check()
    refill_window.show(wait=True)

def back_window4():
    refill_window.hide()

def open_window5():
    random_code =  "".join(random.choice(string.ascii_letters) for _ in range(3))+"".join(random.choice(string.digits) for _ in range(3))
    caregiver_code.value = f"Your caregiver code is: {random_code}"
    with open("/home/pi/Documents/Medbox_GUI/data.json") as f:
        data = json.load(f)
    # print(data)
    header = {"jwt":data["data"]["jwt"]}
    body = {"password":random_code,"medboxID":"1"}
    # print(header)
    # print(body)
    response2 = requests.post("http://3.0.17.207:4000/onboard/register", body,header)
    caregiver_response_data = response2.json()
    with open("caregiver_response_data.json", "w") as f:
        json.dump(caregiver_response_data, f)

    code_window.show(wait=True)


def back_window5():
    code_window.hide()

def back_window_scan():
    scan_window.hide()

def back_window_quantity():
    quantity_window.hide()

def back_window6():
    setting_window.hide()

def save_data():
    f=open("/home/pi/Documents/Medbox_GUI/medbox_data.txt","w")
    f.write(my_name.value+"\n")
    f.close

def open_menu():
    menu_window.show(wait=True)

def setting():
    setting_window.show(wait=True)

def finish_dis():
    global timer_1
    global timer_2
    if DIST.value==0:
        dispense_window.info("Notificaiton", "Please take out the cup first")
    else:
        stop_alarm()
        timer_1.cancel()
        timer_2.cancel()
        dispense_window.hide()

def medicine_info_check():
    with open("/home/pi/Documents/Medbox_GUI/container.json") as f:
        data = json.load(f)
    medicine_name1.value=data["container_1"]["medicine"]["name"]
    medicine_name2.value=data["container_2"]["medicine"]["name"]
    medicine_name3.value=data["container_3"]["medicine"]["name"]
    medicine_name4.value=data["container_4"]["medicine"]["name"]
    medicine_name5.value=data["container_5"]["medicine"]["name"]
    medicine_name6.value=data["container_6"]["medicine"]["name"]
    medicine_name7.value=data["container_7"]["medicine"]["name"]
    medicine_name8.value=data["container_8"]["medicine"]["name"]
    medicine_name9.value=data["container_9"]["medicine"]["name"]
    medicine_name10.value=data["container_10"]["medicine"]["name"]
    medicine_name11.value=data["container_11"]["medicine"]["name"]
    medicine_name12.value=data["container_12"]["medicine"]["name"]
    medicine_quantity1.value=data["container_1"]["quantity_left"]
    medicine_quantity2.value=data["container_2"]["quantity_left"]
    medicine_quantity3.value=data["container_3"]["quantity_left"]
    medicine_quantity4.value=data["container_4"]["quantity_left"]
    medicine_quantity5.value=data["container_5"]["quantity_left"]
    medicine_quantity6.value=data["container_6"]["quantity_left"]
    medicine_quantity7.value=data["container_7"]["quantity_left"]
    medicine_quantity8.value=data["container_8"]["quantity_left"]
    medicine_quantity9.value=data["container_9"]["quantity_left"]
    medicine_quantity10.value=data["container_10"]["quantity_left"]
    medicine_quantity11.value=data["container_11"]["quantity_left"]
    medicine_quantity12.value=data["container_12"]["quantity_left"]

def submit_setting():
    global timer
    slot_dict = {}
    slot_dict["morn"]=pm_to_am(morn_set.value)
    slot_dict["noon"]=pm_to_am(noon_set.value)
    slot_dict["after"]=pm_to_am(after_set.value)
    slot_dict["even"]=pm_to_am(even_set.value)
    with open("/home/pi/Documents/Medbox_GUI/slot.json","w") as f:
        json.dump(slot_dict,f)
    if timer != 0:
        timer.cancel()
    set_timer()
    setting_window.info("Info", "Your changes have been saved")
    setting_window.hide()
    menu_window.show(wait=True)

def set_timer():
    global timer
    file_exist_time = os.path.isfile("slot.json") 
    if file_exist_time:
        now_time = datetime.datetime.now()
        now_year = now_time.date().year
        now_month = now_time.date().month
        now_day = now_time.date().day
        with open("/home/pi/Documents/Medbox_GUI/slot.json") as f:
            data = json.load(f)
        next_list=[]
        morn_hms = data["morn"]
        morn_str = " " + morn_hms[0] + ":" + morn_hms[1] + ":" + "00"
        morn_time = datetime.datetime.strptime(str(now_year)+"-"+str(now_month)+"-"+str(now_day)+morn_str, "%Y-%m-%d %H:%M:%S")
        morn_sec = (morn_time - now_time).total_seconds()
        next_list.append(morn_sec)
        noon_hms = data["noon"]
        noon_str = " " + noon_hms[0] + ":" + noon_hms[1] + ":" + "00"
        noon_time = datetime.datetime.strptime(str(now_year)+"-"+str(now_month)+"-"+str(now_day)+noon_str, "%Y-%m-%d %H:%M:%S")
        noon_sec = (noon_time - now_time).total_seconds()
        next_list.append(noon_sec)
        after_hms = data["after"]
        after_str = " " + after_hms[0] + ":" + after_hms[1] + ":" + "00"
        after_time = datetime.datetime.strptime(str(now_year)+"-"+str(now_month)+"-"+str(now_day)+after_str, "%Y-%m-%d %H:%M:%S")
        after_sec = (after_time - now_time).total_seconds()
        next_list.append(after_sec)
        even_hms = data["even"]
        even_str = " " + even_hms[0] + ":" + even_hms[1] + ":" + "00"
        even_time = datetime.datetime.strptime(str(now_year)+"-"+str(now_month)+"-"+str(now_day)+even_str, "%Y-%m-%d %H:%M:%S")
        even_sec = (even_time - now_time).total_seconds()
        next_list.append(even_sec)
        next_time = now_time + datetime.timedelta(days=+1)
        next_year = next_time.date().year
        next_month = next_time.date().month
        next_day = next_time.date().day
        next_morn = datetime.datetime.strptime(str(next_year)+"-"+str(next_month)+"-"+str(next_day)+morn_str, "%Y-%m-%d %H:%M:%S")
        next_morn_sec = (next_morn - now_time).total_seconds()
        next_list.append(next_morn_sec)
        for i in next_list:
            # print(i)
            if i > 0:
                timer_start_time = i
                break
        timer = threading.Timer(timer_start_time, dispense_all)
        timer.start()

def back_window_wifi():
    wifi_window.hide()


def submit_wifi():
    global wifi
    wifi.connect(wifi_name.value,wifi_password.value)
    if check_ping() == True:  
        file_exists = os.path.isfile("data.json") 
        # print(file_exists)
        if file_exists:
            # f = open("data.json", "r")
            # if f.read() == "":
            #     login_window.show(wait=True)
            #     f.close
            # else:
            with open("/home/pi/Documents/Medbox_GUI/data.json") as f:
                data = json.load(f)
            if data["success"]==1:
                menu_window.show(wait=True)
                menu_window.set_full_screen()
                wifi_window.hide()
            else:
                login_window.show(wait=True)
                wifi_window.hide()
        else:
            # f = open("data.json", "w")
            # f.write("")
            # f.close
            login_window.show(wait=True)
            wifi_window.hide()

    else:
        wifi_window.info("Notificaiton", "Cannot connect to this wifi, please check password")


app = App(title="Homepage",bg = (255,255,224))
app.set_full_screen()
app.hide()
login_window = Window(app, title="Login",bg = (255,255,224),width = 1500, height = 1000)
# login_window.set_full_screen()
login_window.hide()

menu_window = Window(app, title="Menu",bg = (255,255,224))
menu_window.hide()

file_exists = os.path.isfile("data.json") 
# print(file_exists)
if file_exists:
    # f = open("data.json", "r")
    # if f.read() == "":
    #     f.close
    #     app.show()
    # else:
    with open("/home/pi/Documents/Medbox_GUI/data.json") as f:
        data = json.load(f)
    if data["success"]==1:
        app.show()
        # app.set_full_screen()
    else:
        app.show() 
else:
    app.show()




add_med_window = Window(app, title="Add Medicine Window",bg = (255,255,224))
add_med_window.set_full_screen()
add_med_window.hide()
quit_med_window = Window(app, title="Quit Medicine Window",bg = (255,255,224))
quit_med_window.set_full_screen()
quit_med_window.hide()
check_pre_window = Window(app, title="Check Prescription Window",bg = (255,255,224))
check_pre_window.set_full_screen()
check_pre_window.hide()
refill_window = Window(app, title="Refill",bg = (255,255,224))
refill_window.set_full_screen()
refill_window.hide()

code_window = Window(app, title="Code",bg = (255,255,224))
code_window.set_full_screen()
code_window.hide()

setting_window = Window(app, title="Setting",bg = (255,255,224))
setting_window.set_full_screen()
setting_window.hide()

scan_window = Window(app, title="Scan",bg = (255,255,224))
scan_window.set_full_screen()
scan_window.hide()
scan_txt = Text(scan_window,text="Please scan barcode of medicine to proceed",size=80)

confirm_finish_window = Window(app, title="Confirm finish",bg = (255,255,224))
confirm_finish_window.set_full_screen()
confirm_finish_window.hide()
confirm_finish_txt = Text(confirm_finish_window,text="Do you want to refill other medicines?")
finish_yes = PushButton(confirm_finish_window, text ="Yes", command=finish_yes_func)
finish_no = PushButton(confirm_finish_window, text ="No", command=finish_no_func)

#WIFI window
wifi_window = Window(app,title="Wifi",bg = (255,255,224),width = 1500, height = 1000)
wifi_window.hide()
print(wifi.scan())
wifi_name_list=wifi.scan()
if len(wifi_name_list)<10:
    for i in range(10-len(wifi_name_list)):
        wifi_name_list.append("")
# print(wifi.scan())
# print(wifi.connect("WT", "15168877330"))
blank_text10=Text(wifi_window,text="",width="fill")
select_wifi_txt = Text(wifi_window, text="Please select your wifi",size=70)
wifi_name = Combo(wifi_window, options=[wifi_name_list[0],wifi_name_list[1],wifi_name_list[2],wifi_name_list[3],wifi_name_list[4],wifi_name_list[5],wifi_name_list[6],wifi_name_list[7],wifi_name_list[8],wifi_name_list[9]],width=20)
wifi_name.bg =(232, 240, 254)
wifi_name.text_size=50
blank_text11=Text(wifi_window,text="",width="fill")
wifi_password_text = Text(wifi_window, text="Please type in wifi password",size=70)
wifi_password = TextBox(wifi_window,width = 20)
wifi_password.bg=(232, 240, 254)
wifi_password.text_size=70

blank_text4 = Text(wifi_window,text="",size=80)

submit_button = PushButton(wifi_window, text="Submit",command=submit_wifi, width=10)
submit_button.bg=(152,251,152)
submit_button.text_size=50
blank_text12=Text(wifi_window,text="",width="fill",align="bottom")
back_button1 = PushButton(wifi_window, text="Back", command=back_window_wifi, width=10,align="bottom")
back_button1.bg=(255,160,122)
back_button1.text_size=50

#Dispense window
dispense_window = Window(app,title="Dispense",bg =(255,255,224))
dispense_window.set_full_screen()
dispense_window.hide()

blank_text_n1=Text(dispense_window,text="",width="fill",height=2)
dispense_box1 = Box(dispense_window,align="top",width="fill")
medicine_txt1_dis = Text(dispense_box1, text="Medicine",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box1,text="",align="left",width=15)
quantity_txt1_dis = Text(dispense_box1, text="Quantity",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box1,text="",align="left",width=15)
medicine_txt2_dis = Text(dispense_box1, text="Medicine",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box1,text="",align="left",width=15)
quantity_txt2_dis = Text(dispense_box1, text="Quantity",width="fill",align="left",height=2,size=20)

# blank_text_n3=Text(dispense_window,text="",width="fill",height=7)
dispense_box2 = Box(dispense_window,align="top",width="fill")
medicine_name1_dis = Text(dispense_box2, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box2,text="",align="left",width=15)
medicine_quantity1_dis = Text(dispense_box2, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box2,text="",align="left",width=15)
medicine_name2_dis = Text(dispense_box2, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box2,text="",align="left",width=15)
medicine_quantity2_dis = Text(dispense_box2, text="",width="fill",align="left",height=2,size=20)

dispense_box3 = Box(dispense_window,align="top",width="fill")
medicine_name3_dis = Text(dispense_box3, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box3,text="",align="left",width=15)
medicine_quantity3_dis = Text(dispense_box3, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box3,text="",align="left",width=15)
medicine_name4_dis = Text(dispense_box3, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box3,text="",align="left",width=15)
medicine_quantity4_dis = Text(dispense_box3, text="",width="fill",align="left",height=2,size=20)

dispense_box4 = Box(dispense_window,align="top",width="fill")
medicine_name5_dis = Text(dispense_box4, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box4,text="",align="left",width=15)
medicine_quantity5_dis = Text(dispense_box4, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box4,text="",align="left",width=15)
medicine_name6_dis = Text(dispense_box4, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box4,text="",align="left",width=15)
medicine_quantity6_dis = Text(dispense_box4, text="",width="fill",align="left",height=2,size=20)

dispense_box5 = Box(dispense_window,align="top",width="fill")
medicine_name7_dis = Text(dispense_box5, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box5,text="",align="left",width=15)
medicine_quantity7_dis = Text(dispense_box5, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box5,text="",align="left",width=15)
medicine_name8_dis = Text(dispense_box5, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box5,text="",align="left",width=15)
medicine_quantity8_dis = Text(dispense_box5, text="",width="fill",align="left",height=2,size=20)

dispense_box6 = Box(dispense_window,align="top",width="fill")
medicine_name9_dis = Text(dispense_box6, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box6,text="",align="left",width=15)
medicine_quantity9_dis = Text(dispense_box6, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box6,text="",align="left",width=15)
medicine_name10_dis = Text(dispense_box6, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box6,text="",align="left",width=15)
medicine_quantity10_dis = Text(dispense_box6, text="",width="fill",align="left",height=2,size=20)

dispense_box7 = Box(dispense_window,align="top",width="fill")
medicine_name11_dis = Text(dispense_box7, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(dispense_box7,text="",align="left",width=15)
medicine_quantity11_dis = Text(dispense_box7, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(dispense_box7,text="",align="left",width=15)
medicine_name12_dis = Text(dispense_box7, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(dispense_box7,text="",align="left",width=15)
medicine_quantity12_dis = Text(dispense_box7, text="",width="fill",align="left",height=2,size=20)

finish_dispense_btn = PushButton(dispense_window,text="Finish",command=finish_dis,width=15)
finish_dispense_btn.bg=(152,251,152)
finish_dispense_btn.text_size=50

# back_button_scan = PushButton(scan_window, text ="Back", command=back_window_scan, width=15,align="bottom")
# back_button_scan.bg=(255,160,122)
# back_button_scan.text_size=50

quantity_window = Window(app, title="Scan",bg = (255,255,224))
quantity_window.set_full_screen()
quantity_window.hide()
blank_text_nb2=Text(quantity_window,text="",width="fill",height=2)
quantity_no_info = Text(quantity_window,text="Please input the quantity of the medicine refilled",size=50)
refilling_quantity = Text(quantity_window,text="",size=50)

quantity_box1 = Box(quantity_window,align="top",width="fill")
blank_text6=Text(quantity_box1,text="",align="left",width=21)
minus_ten_btn = PushButton(quantity_box1, command=minus_ten, text="-10",width=5,align="left",height=2)
minus_ten_btn.bg=(135,206,250)
minus_ten_btn.text_size=20
blank_text6=Text(quantity_box1,text="",align="left",width=14)
minus_five_btn = PushButton(quantity_box1, command=minus_five, text="-5"  ,width=5,align="left",height=2)
minus_five_btn.bg=(135,206,250)
minus_five_btn.text_size=20
blank_text6=Text(quantity_box1,text="",align="left",width=14)
minus_one_btn = PushButton(quantity_box1, command=minus_one, text="-1"  ,width=5,align="left",height=2)
minus_one_btn.bg=(135,206,250)
minus_one_btn.text_size=20
blank_text6=Text(quantity_box1,text="",align="left",width=14)
quantity_no = Text(quantity_box1,text="0",align="left",size=30)
blank_text6=Text(quantity_box1,text="",align="left",width=14)
add_one_btn = PushButton(quantity_box1, text ="+1", command=add_one,width=5,align="left",height=2)
add_one_btn.bg=(135,206,250)
add_one_btn.text_size=20
blank_text6=Text(quantity_box1,text="",align="left",width=14)
add_five_btn = PushButton(quantity_box1, text ="+5", command=add_five,width=5,align="left",height=2)
add_five_btn.bg=(135,206,250)
add_five_btn.text_size=20
blank_text6=Text(quantity_box1,text="",align="left",width=14)
add_ten_btn = PushButton(quantity_box1, text ="+10", command=add_ten,width=5,align="left",height=2)
add_ten_btn.bg=(135,206,250)
add_ten_btn.text_size=20
# quantity_no = Text(quantity_window,text="0")
# minus_one_btn = PushButton(quantity_window, text ="-1", command=minus_one)
# minus_five_btn = PushButton(quantity_window, text ="-5", command=minus_five)
# minus_ten_btn = PushButton(quantity_window, text ="-10", command=minus_ten)
# add_one_btn = PushButton(quantity_window, text ="+1", command=add_one)
# add_five_btn = PushButton(quantity_window, text ="+5", command=add_five)
# add_ten_btn = PushButton(quantity_window, text ="+10", command=add_ten)
blank_text_n1=Text(quantity_window,text="",height=10)
submit_quan_btn = PushButton(quantity_window, text ="Submit", command=confirm_finish, width=15)
submit_quan_btn.bg=(152,251,152)
submit_quan_btn.text_size=50
back_button_quantity = PushButton(quantity_window, text ="Back", command=back_window_quantity, width=15,align="bottom")
back_button_quantity.bg = (255,160,122)
back_button_quantity.text_size = 50

blank_text9=Text(app,text="",width="fill",height=6)
welcome_text = Text(app,text="Welcome to use the Smart Medbox",size=80)
blank_text1 = Text(app,text="",height=8)
login_button = PushButton(app, command=get_started, text="Get started", width=20,height=3)
login_button.bg=(135,206,250)
login_button.text_size = 60

blank_text10=Text(login_window,text="",width="fill")
ask_name_text = Text(login_window, text="Please type in your username",size=70)
my_name = TextBox(login_window,width = 25)
my_name.bg =(232, 240, 254)
my_name.text_size=70
blank_text11=Text(login_window,text="",width="fill")
ask_password_text = Text(login_window, text="Please type in your password",size=70)
my_password = TextBox(login_window,width = 25)
my_password.bg=(232, 240, 254)
my_password.text_size=70

blank_text4 = Text(login_window,text="",size=80)

submit_button = PushButton(login_window, text="Submit",command=submit, width=10)
submit_button.bg=(152,251,152)
submit_button.text_size=50
blank_text12=Text(login_window,text="",width="fill",align="bottom")
back_button1 = PushButton(login_window, text="Back", command=back_window_login, width=10,align="bottom")
back_button1.bg=(255,160,122)
back_button1.text_size=50

blank_text5=Text(menu_window,text="",width="fill",height=6)
menu_box1 = Box(menu_window,align="top",width="fill")
refill = PushButton(menu_box1, command=open_window4, text="Refill Medicine",width=17,align="left",height=2)
refill.bg=(135,206,250)
refill.text_size=50
blank_text6=Text(menu_box1,text="",align="left",width=40)
check_pre = PushButton(menu_box1, command=open_window3, text="Check Prescription",width=17,align="left",height=2)
check_pre.bg=(135,206,250)
check_pre.text_size=50
# quit_med_button = PushButton(menu_box1, command=open_window2, text="Quit Medicine"  ,width="fill",align="left",height=2)
# quit_med_button.bg=(135,206,250)
# quit_med_button.text_size=50

blank_text7=Text(menu_window,text="",width="fill",height=10)
menu_box2 = Box(menu_window,align="top",width="fill")
add_caregiver_code = PushButton(menu_box2, command=open_window5, text="Caregiver Code",width=17,align="left",height=2)
add_caregiver_code.bg=(135,206,250)
add_caregiver_code.text_size=50
blank_text8=Text(menu_box2,text="",align="left",width=40)
setting_button = PushButton(menu_box2, command=setting, text="Setting",width=17,align="left",height=2)
setting_button.bg=(135,206,250)
setting_button.text_size=50

# blank_text9=Text(menu_window,text="",width="fill",height=7)
# menu_box3 = Box(menu_window,align="top",width="fill")
# setting_button = PushButton(menu_box3, command=setting, text="Setting",width=15,align="left",height=2)
# setting_button.bg=(135,206,250)
# setting_button.text_size=50
# blank_text16=Text(menu_box3,text="",align="left",width=70)

# ask_med_text = Text(add_med_window, text="Please type in your medicine name")
# med_name = TextBox(add_med_window)
# next_button = PushButton(add_med_window,text="Next",command=save_data, width=15)
back_button2 = PushButton(add_med_window, text="Back", command=back_window1, width=15,align="bottom")
back_button2.bg=(255,160,122)
back_button2.text_size=50
back_button3 = PushButton(quit_med_window, text="Back", command=back_window2, width=15,align="bottom")
back_button3.bg=(255,160,122)
back_button3.text_size=50
back_button4 = PushButton(check_pre_window, text="Back", command=back_window3, width=15,align="bottom")
back_button4.bg=(255,160,122)
back_button4.text_size=50

check_pre_box1 = Box(check_pre_window,align="top",width="fill")
medicine_txt1_chepre = Text(check_pre_box1, text="Medicine",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box1,text="",align="left",width=10)
medicine_txt1_chepre = Text(check_pre_box1, text="Dose",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box1,text="",align="left",width=15)
message_txt1_chepre = Text(check_pre_box1, text="Message",width=35,align="left",height=2,size=20)
check_pre_box2 = Box(check_pre_window,align="top",width="fill")
medicine_name1_chepre = Text(check_pre_box2, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box2,text="",align="left",width=10)
medicine_dose1_chepre = Text(check_pre_box2, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box2,text="",align="left",width=15)
medicine_message1_chepre = Text(check_pre_box2, text="",width=35,align="left",height=2,size=20)
check_pre_box3 = Box(check_pre_window,align="top",width="fill")
medicine_name2_chepre = Text(check_pre_box3, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box3,text="",align="left",width=10)
medicine_dose2_chepre = Text(check_pre_box3, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box3,text="",align="left",width=15)
medicine_message2_chepre = Text(check_pre_box3, text="",width=35,align="left",height=2,size=20)
check_pre_box4 = Box(check_pre_window,align="top",width="fill")
medicine_name3_chepre = Text(check_pre_box4, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box4,text="",align="left",width=10)
medicine_dose3_chepre = Text(check_pre_box4, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box4,text="",align="left",width=15)
medicine_message3_chepre = Text(check_pre_box4, text="",width=35,align="left",height=2,size=20)
check_pre_box5 = Box(check_pre_window,align="top",width="fill")
medicine_name4_chepre = Text(check_pre_box5, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box5,text="",align="left",width=10)
medicine_dose4_chepre = Text(check_pre_box5, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box5,text="",align="left",width=15)
medicine_message4_chepre = Text(check_pre_box5, text="",width=35,align="left",height=2,size=20)
check_pre_box6 = Box(check_pre_window,align="top",width="fill")
medicine_name5_chepre = Text(check_pre_box6, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box6,text="",align="left",width=10)
medicine_dose5_chepre = Text(check_pre_box6, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box6,text="",align="left",width=15)
medicine_message5_chepre = Text(check_pre_box6, text="",width=35,align="left",height=2,size=20)
check_pre_box7 = Box(check_pre_window,align="top",width="fill")
medicine_name6_chepre = Text(check_pre_box7, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box7,text="",align="left",width=10)
medicine_dose6_chepre = Text(check_pre_box7, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box7,text="",align="left",width=15)
medicine_message6_chepre = Text(check_pre_box7, text="",width=35,align="left",height=2,size=20)
check_pre_box8 = Box(check_pre_window,align="top",width="fill")
medicine_name7_chepre = Text(check_pre_box8, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box8,text="",align="left",width=10)
medicine_dose7_chepre = Text(check_pre_box8, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box8,text="",align="left",width=15)
medicine_message7_chepre = Text(check_pre_box8, text="",width=35,align="left",height=2,size=20)
check_pre_box9 = Box(check_pre_window,align="top",width="fill")
medicine_name8_chepre = Text(check_pre_box9, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box9,text="",align="left",width=10)
medicine_dose8_chepre = Text(check_pre_box9, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box9,text="",align="left",width=15)
medicine_message8_chepre = Text(check_pre_box9, text="",width=35,align="left",height=2,size=20)
check_pre_box10 = Box(check_pre_window,align="top",width="fill")
medicine_name9_chepre = Text(check_pre_box10, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box10,text="",align="left",width=10)
medicine_dose9_chepre = Text(check_pre_box10, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box10,text="",align="left",width=15)
medicine_message9_chepre = Text(check_pre_box10, text="",width=35,align="left",height=2,size=20)
check_pre_box11 = Box(check_pre_window,align="top",width="fill")
medicine_name10_chepre = Text(check_pre_box11, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box11,text="",align="left",width=10)
medicine_dose10_chepre = Text(check_pre_box11, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box11,text="",align="left",width=15)
medicine_message10_chepre = Text(check_pre_box11, text="",width=35,align="left",height=2,size=20)
check_pre_box12 = Box(check_pre_window,align="top",width="fill")
medicine_name11_chepre = Text(check_pre_box12, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box12,text="",align="left",width=10)
medicine_dose11_chepre = Text(check_pre_box12, text="",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box12,text="",align="left",width=15)
medicine_message11_chepre = Text(check_pre_box12, text="",width=35,align="left",height=2,size=20)
check_pre_box13 = Box(check_pre_window,align="top",width="fill")
medicine_name12_chepre = Text(check_pre_box13, text="1",width=35,align="left",height=2,size=20)
blank_text_n2=Text(check_pre_box13,text="",align="left",width=10)
medicine_dose12_chepre = Text(check_pre_box13, text="1",width=35,align="left",height=2,size=20)
blank_text_n6=Text(check_pre_box13,text="",align="left",width=15)
medicine_message12_chepre = Text(check_pre_box13, text="1",width=35,align="left",height=2,size=20)

#refill window
blank_text_n1=Text(refill_window,text="",width="fill",height=2)
refill_box1 = Box(refill_window,align="top",width="fill")
medicine_txt1 = Text(refill_box1, text="Medicine",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box1,text="",align="left",width=15)
quantity_txt1 = Text(refill_box1, text="Quantity",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box1,text="",align="left",width=15)
medicine_txt2 = Text(refill_box1, text="Medicine",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box1,text="",align="left",width=15)
quantity_txt2 = Text(refill_box1, text="Quantity",width="fill",align="left",height=2,size=20)

# blank_text_n3=Text(refill_window,text="",width="fill",height=7)
refill_box2 = Box(refill_window,align="top",width="fill")
medicine_name1 = Text(refill_box2, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box2,text="",align="left",width=15)
medicine_quantity1 = Text(refill_box2, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box2,text="",align="left",width=15)
medicine_name2 = Text(refill_box2, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box2,text="",align="left",width=15)
medicine_quantity2 = Text(refill_box2, text="",width="fill",align="left",height=2,size=20)

# blank_text_n3=Text(refill_window,text="",width="fill",height=7)
refill_box3 = Box(refill_window,align="top",width="fill")
medicine_name3 = Text(refill_box3, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box3,text="",align="left",width=15)
medicine_quantity3 = Text(refill_box3, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box3,text="",align="left",width=15)
medicine_name4 = Text(refill_box3, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box3,text="",align="left",width=15)
medicine_quantity4 = Text(refill_box3, text="",width="fill",align="left",height=2,size=20)

refill_box4 = Box(refill_window,align="top",width="fill")
medicine_name5 = Text(refill_box4, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box4,text="",align="left",width=15)
medicine_quantity5 = Text(refill_box4, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box4,text="",align="left",width=15)
medicine_name6 = Text(refill_box4, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box4,text="",align="left",width=15)
medicine_quantity6 = Text(refill_box4, text="",width="fill",align="left",height=2,size=20)

refill_box5 = Box(refill_window,align="top",width="fill")
medicine_name7 = Text(refill_box5, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box5,text="",align="left",width=15)
medicine_quantity7 = Text(refill_box5, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box5,text="",align="left",width=15)
medicine_name8 = Text(refill_box5, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box5,text="",align="left",width=15)
medicine_quantity8 = Text(refill_box5, text="",width="fill",align="left",height=2,size=20)

refill_box6 = Box(refill_window,align="top",width="fill")
medicine_name9 = Text(refill_box6, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box6,text="",align="left",width=15)
medicine_quantity9 = Text(refill_box6, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box6,text="",align="left",width=15)
medicine_name10 = Text(refill_box6, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box6,text="",align="left",width=15)
medicine_quantity10 = Text(refill_box6, text="",width="fill",align="left",height=2,size=20)

refill_box7 = Box(refill_window,align="top",width="fill")
medicine_name11 = Text(refill_box7, text="",width=35,align="left",height=2,size=20)
blank_text_n2=Text(refill_box7,text="",align="left",width=15)
medicine_quantity11 = Text(refill_box7, text="",width="fill",align="left",height=2,size=20)
blank_text_n6=Text(refill_box7,text="",align="left",width=15)
medicine_name12 = Text(refill_box7, text="",width=35,align="left",height=2,size=20)
blank_text_n7=Text(refill_box7,text="",align="left",width=15)
medicine_quantity12 = Text(refill_box7, text="",width="fill",align="left",height=2,size=20)

med_list = [[medicine_name1,medicine_quantity1],[medicine_name2,medicine_quantity2],[medicine_name3,medicine_quantity3],[medicine_name4,medicine_quantity4],[medicine_name5,medicine_quantity5],[medicine_name6,medicine_quantity6],[medicine_name7,medicine_quantity7],[medicine_name8,medicine_quantity8],[medicine_name9,medicine_quantity9],[medicine_name10,medicine_quantity10],[medicine_name11,medicine_quantity11],[medicine_name12,medicine_quantity12]]
blank_text_bfscan = Text(refill_window,text="",height=10)
scan_button = PushButton(refill_window, text = "Scan barcode", command = refillProcess, width=15)
# submit_set_button = PushButton(setting_window, text="Submit",command=submit_setting, width=10)
scan_button.bg=(152,251,152)
scan_button.text_size=50
back_button5 = PushButton(refill_window, text="Back", command=back_window4, width=15,align="bottom")
back_button5.bg=(255,160,122)
back_button5.text_size=50

blank_text14=Text(code_window,text="",width="fill")
medbox_id = Text(code_window, text="Your medbox id is: 1",size=70)
blank_text15=Text(code_window,text="",width="fill")
caregiver_code = Text(code_window, text=f"Your caregiver code is: {random_code}",size=70)
blank_text13=Text(code_window,text="",width="fill",align="bottom")
back_button6 = PushButton(code_window, text="Back", command=back_window5, width=15,align="bottom")
back_button6.bg=(255,160,122)
back_button6.text_size=50

blank_text18=Text(setting_window,text="",width="fill")
default_text = Text(setting_window, text="Please select your default time sessions",size=60,align="top")
tip_text = Text(setting_window, text="(Press the button to select)",size=40,align="top")
blank_text23=Text(setting_window,text="",width="fill",height=4)

time_box1 = Box(setting_window,align="top",width="fill")

blank_text24=Text(time_box1,text="",align="left",width=18)
morn_text = Text(time_box1, text="Morning:",size=40,align="left")
blank_text210=Text(time_box1,text="",align="left",width=29)
noon_text = Text(time_box1, text="Noon:",size=40,align="left")
blank_text26=Text(time_box1,text="",align="left",width=29)
after_text = Text(time_box1, text="Afternoon:",size=40,align="left")
blank_text27=Text(time_box1,text="",align="left",width=24)
even_text = Text(time_box1, text="Evening:",size=40,align="left")
blank_text28=Text(time_box1,text="",align="left",width=23)

blank_text34=Text(setting_window,text="",align="top",width="fill")

time_box2 = Box(setting_window,align="top",width="fill")

blank_text29=Text(time_box2,text="",align="left",width=8)
morn_set = Combo(time_box2, options=["5:00AM", "5:30AM", "6:00AM", "6:30AM", "7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM"],align="left",width=10)
morn_set.bg =(232, 240, 254)
morn_set.text_size=40
blank_text30=Text(time_box2,text="",align="left",width=8)
noon_set = Combo(time_box2, options=["10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30AM"],align="left",width=10)
noon_set.bg =(232, 240, 254)
noon_set.text_size=40
blank_text31=Text(time_box2,text="",align="left",width=8)
after_set = Combo(time_box2, options=["1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM"],align="left",width=10)
after_set.bg =(232, 240, 254)
after_set.text_size=40
blank_text32=Text(time_box2,text="",align="left",width=8)
even_set = Combo(time_box2, options=["5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM", "10:30PM"],align="left",width=10)
even_set.bg =(232, 240, 254)
even_set.text_size=40
blank_text33=Text(time_box2,text="",align="left",width=8)

blank_text21 = Text(setting_window,text="",height=8)
submit_set_button = PushButton(setting_window, text="Submit",command=submit_setting, width=10)
submit_set_button.bg=(152,251,152)
submit_set_button.text_size=50
blank_text17=Text(setting_window,text="",width="fill",align="bottom")
back_button7 = PushButton(setting_window, text="Back", command=back_window6, width=10,align="bottom")
back_button7.bg=(255,160,122)
back_button7.text_size=50

medicine_info_check()
set_timer()

app.display()