from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window, info, Box
import requests 
import json
import base64
import random
import string
import os.path

random_code = ""

def get_started():
    file_exists = os.path.isfile('data.json') 
    # print(file_exists)
    if file_exists:
        f = open("data.json", "r")
        if f.read() == "":
            login_window.show(wait=True)
            f.close
        else:
            with open('/home/pi/Documents/Medbox_GUI/data.json') as f:
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
    #         app.info("Error", "Cannot connect to the database")
    #     elif data["error"] == "no such user exists":
    #         app.info("Error", "This is not a valid account")
    #     elif data["error"] == "username and passowrd did not match":
    #         app.info("Error", "Username and passowrd do not match")
    menu_window.show(wait=True)
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
    # with open('/home/pi/Doucments/data.json') as f:
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

def save_data():
    f=open('/home/pi/Documents/Medbox_GUI/medbox_data.txt','w')
    f.write(my_name.value+'\n')
    f.close

def open_menu():
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
        with open('/home/pi/Documents/Medbox_GUI/data.json') as f:
            data = json.load(f)
        if data["success"]==1:
            menu_window.show(wait=True)
else:
    f = open("data.json", "w")
    f.write("")
    f.close
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
emergency_window = Window(app, title="Emergency Window",bg = (255,255,224))
emergency_window.set_full_screen()
emergency_window.hide()
code_window = Window(app, title="Code",bg = (255,255,224))
code_window.set_full_screen()
code_window.hide()

welcome_text = Text(app,text="Welcome to use the Smart Medbox",size=80)
blank_text1 = Text(app,text="",size=80)
blank_text2 = Text(app,text="",size=80)
blank_text3 = Text(app,text="",size=50)
login_button = PushButton(app, command=get_started, text="Get started", width=20)
login_button.bg=(135,206,250)
login_button.text_size = 60

ask_name_text = Text(login_window, text="Please type in your username",size=70)
my_name = TextBox(login_window,width = 25)
my_name.bg =(232, 240, 254)
my_name.text_size=70
ask_password_text = Text(login_window, text="Please type in your password",size=70)
my_password = TextBox(login_window,width = 25)
my_password.bg=(232, 240, 254)
my_password.text_size=70

blank_text4 = Text(login_window,text="",size=80)

submit_button = PushButton(login_window, text="Submit",command=submit, width=10)
submit_button.bg=(152,251,152)
submit_button.text_size=50
back_button1 = PushButton(login_window, text="Back", command=back_window_login, width=10,align="bottom")
back_button1.bg=(255,160,122)
back_button1.text_size=50

blank_text5=Text(menu_window,text="",width="fill",height=5)
menu_box1 = Box(menu_window,align="top",width="fill")
add_med_button = PushButton(menu_box1, command=open_window1, text="Add Medicine" ,width=15,align="left",height=2)
add_med_button.bg=(135,206,250)
add_med_button.text_size=50
blank_text6=Text(menu_box1,text="",align="left",width=40)
quit_med_button = PushButton(menu_box1, command=open_window2, text="Quit Medicine"  ,width="fill",align="left",height=2)
quit_med_button.bg=(135,206,250)
quit_med_button.text_size=50

blank_text7=Text(menu_window,text="",width="fill",height=5)
menu_box2 = Box(menu_window,align="top",width="fill")
check_pre = PushButton(menu_box2, command=open_window3, text="Check Prescription",width=15,align="left",height=2)
check_pre.bg=(135,206,250)
check_pre.text_size=50
blank_text8=Text(menu_box2,text="",align="left",width=40)
emergency = PushButton(menu_box2, command=open_window4, text="Emergency call",width="fill",align="left",height=2)
emergency.bg=(135,206,250)
emergency.text_size=50

blank_text9=Text(menu_window,text="",width="fill",height=5)
menu_box3 = Box(menu_window,align="top",width="fill")
add_caregiver_code = PushButton(menu_box3, command=open_window5, text="Caregiver Code",width=15,align="left",height=2)
add_caregiver_code.bg=(135,206,250)
add_caregiver_code.text_size=50

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

medbox_id = Text(code_window, text="Your medbox id is: 1",size=70)
caregiver_code = Text(code_window, text=f"Your caregiver code is: {random_code}",size=70)
back_button6 = PushButton(code_window, text="Back", command=back_window5, width=15,align="bottom")
back_button6.bg=(255,160,122)
back_button6.text_size=50

app.display()