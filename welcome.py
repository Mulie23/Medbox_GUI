from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window, info, Box
import requests 
import json
import base64
import random
import string
import os.path
from dispensefunc import dispense
import datetime
import threading

random_code = ""

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
    file_exists = os.path.isfile('data.json') 
    # print(file_exists)
    if file_exists:
        f = open("data.json", "r")
        if f.read() == "":
            login_window.show(wait=True)
            f.close
        else:
            with open('D:/Term 8/Capstone/guizero/Medbox_GUI/data.json') as f:
                data = json.load(f)
            if data["success"]==1:
                menu_window.show(wait=True)
    else:
        f = open("data.json", "w")
        f.write("")
        f.close
        login_window.show(wait=True)




def back_window_login():
    login_window.hide()

def submit():
    # body =  {'username': my_name.value , 'password' : my_password.value }
    # # print(body)
    # response = requests.post('http://3.0.17.207:4000/medboxAuth/login', body)
    # data = response.json()
    # with open('data.json', 'w') as f:
    #     json.dump(data, f)
    # # print(data)
    # if data["success"] == 1:
    #     menu_window.show(wait=True)
    # elif data["success"] == 0:
    #     if data["error"] == "db connection error":
    #         login_screen.info("Error", "Cannot connect to the database")
    #     elif data["error"] == "no such user exists":
    #         login_screen.info("Error", "This is not a valid account")
    #     elif data["error"] == "username and passowrd did not match":
    #         login_screen.info("Error", "Username and passowrd do not match")
    setting_window.show(wait=True)
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
    check_pre_window.show(wait=True)

def back_window3():
    check_pre_window.hide()

def open_window4():
    emergency_window.show(wait=True)

def back_window4():
    emergency_window.hide()

def open_window5():
    random_code =  ''.join(random.choice(string.ascii_letters) for _ in range(3))+''.join(random.choice(string.digits) for _ in range(3))
    caregiver_code.value = f"Your caregiver code is: {random_code}"
    # with open('/home/pi/Doucments/MedBox_GUI/data.json') as f:
    #     data = json.load(f)
    # # print(data)
    # header = {'jwt':data['data']['jwt']}
    # body = {'password':random_code,'medboxID':'1'}
    # print(header)
    # print(body)
    # response2 = requests.post('http://3.0.17.207:4000/onboard/register', body,header)
    code_window.show(wait=True)


def back_window5():
    code_window.hide()

def back_window6():
    setting_window.hide()

def save_data():
    f=open('D:/Term 8/Capstone/guizero/Medbox_GUI/medbox_data.txt','w')
    f.write(my_name.value+'\n')
    f.close

def open_menu():
    menu_window.show(wait=True)

def setting():
    setting_window.show(wait=True)

def submit_setting():
    slot_dict = {}
    slot_dict["morn"]=pm_to_am(morn_set.value)
    slot_dict["noon"]=pm_to_am(noon_set.value)
    slot_dict["after"]=pm_to_am(after_set.value)
    slot_dict["even"]=pm_to_am(even_set.value)
    with open('D:/Term 8/Capstone/guizero/Medbox_GUI/slot.json','w') as f:
        json.dump(slot_dict,f)
    timer.cancel()
    now_time = datetime.datetime.now()
    now_year = now_time.date().year
    now_month = now_time.date().month
    now_day = now_time.date().day
    with open('D:/Term 8/Capstone/guizero/Medbox_GUI/slot.json') as f:
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
        print(i)
        if i > 0:
            timer_start_time = i
            break
    timer1 = threading.Timer(timer_start_time, dispense)
    timer1.start()
    setting_window.info("Info", "Your changes have been saved")
    setting_window.hide()
    menu_window.show(wait=True)



app = App(title="Homepage",bg = (255,255,224))
app.set_full_screen()
app.hide()
login_window = Window(app, title="Login",bg = (255,255,224))
login_window.set_full_screen()
login_window.hide()

menu_window = Window(app, title="Menu",bg = (255,255,224))
menu_window.hide()
menu_window.set_full_screen()
file_exists = os.path.isfile('data.json') 
# print(file_exists)
if file_exists:
    f = open("data.json", "r")
    if f.read() == "":
        app.show()
        f.close
        app.show()
    else:
        with open('D:/Term 8/Capstone/guizero/Medbox_GUI/data.json') as f:
            data = json.load(f)
        if data["success"]==1:
            menu_window.show(wait=True)
else:
    f = open("data.json", "w")
    f.write("")
    f.close
    app.show()



file_exist_time = os.path.isfile('slot.json') 
if file_exist_time:
    now_time = datetime.datetime.now()
    now_year = now_time.date().year
    now_month = now_time.date().month
    now_day = now_time.date().day
    with open('D:/Term 8/Capstone/guizero/Medbox_GUI/slot.json') as f:
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
        print(i)
        if i > 0:
            timer_start_time = i
            break
    timer = threading.Timer(timer_start_time, dispense)
    timer.start()

add_med_window = Window(app, title="Add Medicine Window",bg = (255,255,224))
add_med_window.set_full_screen()
add_med_window.hide()
quit_med_window = Window(app, title="Quit Medicine Window",bg = (255,255,224))
quit_med_window.set_full_screen()
quit_med_window.hide()
check_pre_window = Window(app, title="Check Prescription Window",bg = (255,255,224))
check_pre_window.set_full_screen()
check_pre_window.hide()
emergency_window = Window(app, title="Emergency Window",bg = (255,255,224))
emergency_window.set_full_screen()
emergency_window.hide()
code_window = Window(app, title="Code",bg = (255,255,224))
code_window.set_full_screen()
code_window.hide()
setting_window = Window(app, title="Setting",bg = (255,255,224))
setting_window.set_full_screen()
setting_window.hide()

# blank_text9=Text(app,text="",width="fill",height=6)
welcome_text = Text(app,text="Welcome to use the Smart Medbox",size=80)
# blank_text1 = Text(app,text="",height=8)
login_button = PushButton(app, command=get_started, text="Get started", width=20,height=3)
login_button.bg=(135,206,250)
login_button.text_size = 60

# blank_text10=Text(login_window,text="",width="fill")
ask_name_text = Text(login_window, text="Please type in your username",size=70)
my_name = TextBox(login_window,width = 25)
my_name.bg =(232, 240, 254)
my_name.text_size=70
# blank_text11=Text(login_window,text="",width="fill")
ask_password_text = Text(login_window, text="Please type in your password",size=70)
my_password = TextBox(login_window,width = 25)
my_password.bg=(232, 240, 254)
my_password.text_size=70

# blank_text4 = Text(login_window,text="",size=80)

submit_button = PushButton(login_window, text="Submit",command=submit, width=10)
submit_button.bg=(152,251,152)
submit_button.text_size=50
# blank_text12=Text(login_window,text="",width="fill",align="bottom")
back_button1 = PushButton(login_window, text="Back", command=back_window_login, width=10,align="bottom")
back_button1.bg=(255,160,122)
back_button1.text_size=50

# blank_text5=Text(menu_window,text="",width="fill",height=6)
menu_box1 = Box(menu_window,align="top",width="fill")
add_med_button = PushButton(menu_box1, command=open_window1, text="Add Medicine" ,width=15,align="left",height=2)
add_med_button.bg=(135,206,250)
add_med_button.text_size=50
# blank_text6=Text(menu_box1,text="",align="left",width=70)
quit_med_button = PushButton(menu_box1, command=open_window2, text="Quit Medicine"  ,width="fill",align="left",height=2)
quit_med_button.bg=(135,206,250)
quit_med_button.text_size=50

# blank_text7=Text(menu_window,text="",width="fill",height=7)
menu_box2 = Box(menu_window,align="top",width="fill")
check_pre = PushButton(menu_box2, command=open_window3, text="Check Prescription",width=15,align="left",height=2)
check_pre.bg=(135,206,250)
check_pre.text_size=50
# blank_text8=Text(menu_box2,text="",align="left",width=70)
emergency = PushButton(menu_box2, command=open_window4, text="Emergency call",width="fill",align="left",height=2)
emergency.bg=(135,206,250)
emergency.text_size=50

# blank_text9=Text(menu_window,text="",width="fill",height=7)
menu_box3 = Box(menu_window,align="top",width="fill")
add_caregiver_code = PushButton(menu_box3, command=open_window5, text="Caregiver Code",width=15,align="left",height=2)
add_caregiver_code.bg=(135,206,250)
add_caregiver_code.text_size=50
# blank_text16=Text(menu_box3,text="",align="left",width=70)
setting_button = PushButton(menu_box3, command=setting, text="Setting",width=15,align="left",height=2)
setting_button.bg=(135,206,250)
setting_button.text_size=50
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
back_button5 = PushButton(emergency_window, text="Back", command=back_window4, width=15,align="bottom")
back_button5.bg=(255,160,122)
back_button5.text_size=50

# blank_text14=Text(code_window,text="",width="fill")
medbox_id = Text(code_window, text="Your medbox id is: 1",size=70)
# blank_text15=Text(code_window,text="",width="fill")
caregiver_code = Text(code_window, text=f"Your caregiver code is: {random_code}",size=70)
# blank_text13=Text(code_window,text="",width="fill",align="bottom")
back_button6 = PushButton(code_window, text="Back", command=back_window5, width=15,align="bottom")
back_button6.bg=(255,160,122)
back_button6.text_size=50

# blank_text18=Text(setting_window,text="",width="fill")
default_text = Text(setting_window, text="Please select your default time sessions",size=60,align="top")
tip_text = Text(setting_window, text="(Press the button to select)",size=40,align="top")
# blank_text23=Text(setting_window,text="",width="fill",height=4)

time_box1 = Box(setting_window,align="top",width="fill")

# blank_text24=Text(time_box1,text="",align="left",width=18)
morn_text = Text(time_box1, text="Morning:",size=40,align="left")
# blank_text210=Text(time_box1,text="",align="left",width=29)
noon_text = Text(time_box1, text="Noon:",size=40,align="left")
# blank_text26=Text(time_box1,text="",align="left",width=29)
after_text = Text(time_box1, text="Afternoon:",size=40,align="left")
# blank_text27=Text(time_box1,text="",align="left",width=24)
even_text = Text(time_box1, text="Evening:",size=40,align="left")
# blank_text28=Text(time_box1,text="",align="left",width=23)

# blank_text34=Text(setting_window,text="",align="top",width="fill")

time_box2 = Box(setting_window,align="top",width="fill")

# blank_text29=Text(time_box2,text="",align="left",width=8)
morn_set = Combo(time_box2, options=["5:00AM", "5:30AM", "6:00AM", "6:30AM", "7:00AM", "7:30AM", "8:00AM", "8:30AM", "9:00AM", "9:30AM"],align="left",width=10)
morn_set.bg =(232, 240, 254)
morn_set.text_size=40
# blank_text30=Text(time_box2,text="",align="left",width=8)
noon_set = Combo(time_box2, options=["10:00AM", "10:30AM", "11:00AM", "11:30AM", "12:00PM", "12:30PM", "1:00PM", "1:30PM", "2:00PM", "2:30AM"],align="left",width=10)
noon_set.bg =(232, 240, 254)
noon_set.text_size=40
# blank_text31=Text(time_box2,text="",align="left",width=8)
after_set = Combo(time_box2, options=["1:00PM", "1:30PM", "2:00PM", "2:30PM", "3:00PM", "3:30PM", "4:00PM", "4:30PM", "5:00PM", "5:30PM"],align="left",width=10)
after_set.bg =(232, 240, 254)
after_set.text_size=40
# blank_text32=Text(time_box2,text="",align="left",width=8)
even_set = Combo(time_box2, options=["5:00PM", "5:30PM", "6:00PM", "6:30PM", "7:00PM", "7:30PM", "8:00PM", "8:30PM", "9:00PM", "9:30PM", "10:00PM", "10:30PM"],align="left",width=10)
even_set.bg =(232, 240, 254)
even_set.text_size=40
# blank_text33=Text(time_box2,text="",align="left",width=8)

# blank_text21 = Text(setting_window,text="",height=8)
submit_set_button = PushButton(setting_window, text="Submit",command=submit_setting, width=10)
submit_set_button.bg=(152,251,152)
submit_set_button.text_size=50
# blank_text17=Text(setting_window,text="",width="fill",align="bottom")
back_button7 = PushButton(setting_window, text="Back", command=back_window6, width=10,align="bottom")
back_button7.bg=(255,160,122)
back_button7.text_size=50

app.display()