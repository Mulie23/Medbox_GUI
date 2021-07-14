from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window
import requests 
import json
import base64
import random
import string


random_code =  "".join(random.choice(string.ascii_letters) for _ in range(3))+"".join(random.choice(string.digits) for _ in range(3))

def open_window_login():
    login_window.show(wait=True)

def close_window_login():
    login_window.hide()

def submit():
    body =  {"username": my_name.value , "password" : my_password.value }
    print(body)
    response = requests.post("http://3.0.17.207:4000/medboxAuth/login", body)
    data = response.json()
    with open("data.json", "w") as f:
        json.dump(data, f)
    print(data)
    if data["success"] == 1:
        header = {"jwt":data["data"]["jwt"]}
        body = {"password":random_code,"medboxID":"1"}
        print(header)
        print(body)
        response2 = requests.post("http://3.0.17.207:4000/onboard/register", body,header)
        code_window.show(wait=True)

def add_med():
    pass

def open_window1():
    add_med_window.show(wait=True)

def close_window1():
    add_med_window.hide()

def open_window2():
    quit_med_window.show(wait=True)

def close_window2():
    quit_med_window.hide()

def open_window3():
    check_pre_window.show(wait=True)

def close_window3():
    check_pre_window.hide()

def open_window4():
    emergency_window.show(wait=True)

def close_window4():
    emergency_window.hide()

def save_data():
    f=open("D:/Term 8/Capstone/medbox_data.txt","w")
    f.write(my_name.value+"\n")
    f.close
def open_menu():
    menu_window.show(wait=True)
app = App(title="Homepage",layout="grid", width=476, height=208,bg = "white")
login_window = Window(app, title="Login",layout="grid", width=476, height=208,bg = "white")
login_window.hide()
code_window = Window(app, title="Code",layout="grid", width=476, height=208,bg = "white")
code_window.hide()
menu_window = Window(app, title="Menu",layout="grid", width=476, height=208,bg = "white")
menu_window.hide()
add_med_window = Window(app, title="Add Medicine Window",layout="grid", width=476, height=208,bg = "white")
add_med_window.hide()
quit_med_window = Window(app, title="Quit Medicine Window", width=476, height=208,bg = "white")
quit_med_window.hide()
check_pre_window = Window(app, title="Check Prescription Window", width=476, height=208,bg = "white")
check_pre_window.hide()
emergency_window = Window(app, title="Emergency Window", width=476, height=208,bg = "white")
emergency_window.hide()

welcome_text = Text(app,text="Welcome to use Smart Medbox, please login to proceed", grid=[0,0])
login_button = PushButton(app, command=open_window_login, text="Login", grid=[0,1], width=30, height=5)
ask_name_text = Text(login_window, text="Please type in your username", grid=[0,0])
ask_password_text = Text(login_window, text="Please type in your password", grid=[0,1])
my_name = TextBox(login_window,grid=[1,0])
my_password = TextBox(login_window,grid=[1,1])
submit_button = PushButton(login_window, text="Submit",command=submit, grid=[0,2])
close_button1 = PushButton(login_window, text="Close", command=close_window_login,grid=[1,2])
caregiver_code = Text(code_window, text=f"Your caregiver code is {random_code}", grid=[0,0])
menu_button = PushButton(code_window,text="Next",command=open_menu,grid=[0,1])


add_med_button = PushButton(menu_window, command=open_window1, text="Add Medicine", grid=[0,0], width=30, height=5)
ask_med_text = Text(add_med_window, text="Please type in your medicine name", grid=[0,0])
med_name = TextBox(add_med_window,grid=[1,0])
next_button = PushButton(add_med_window,text="Next",command=save_data,grid=[0,1])
close_button1 = PushButton(add_med_window, text="Close", command=close_window1,grid=[1,1])

quit_med_button = PushButton(menu_window, command=open_window2, text="Quit Medicine", grid=[0,1], width=30, height=5)
close_button2 = PushButton(quit_med_window, text="Close", command=close_window2)
check_pre = PushButton(menu_window, command=open_window3, text="Check Prescription", grid=[1,0], width=30, height=5)
close_button3 = PushButton(check_pre_window, text="Close", command=close_window3)
emergency = PushButton(menu_window, command=open_window4, text="Emergency call", grid=[1,1], width=30, height=5)
close_button4 = PushButton(emergency_window, text="Close", command=close_window4)

app.display()