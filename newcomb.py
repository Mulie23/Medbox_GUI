from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window
import requests 
import json
import base64
import random
import string

random_code = ""

def open_window_login():
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
    #     header = {'jwt':data['data']['jwt']}
    #     body = {'password':random_code,'medboxID':'1'}
    #     # print(header)
    #     # print(body)
    #     response2 = requests.post('http://3.0.17.207:4000/onboard/register', body,header)
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
    code_window.show(wait=True)


def back_window5():
    code_window.hide()

def save_data():
    f=open('D:/Term 8/Capstone/medbox_data.txt','w')
    f.write(my_name.value+'\n')
    f.close

def open_menu():
    menu_window.show(wait=True)

app = App(title="Homepage",bg = "white")
app.set_full_screen()
login_window = Window(app, title="Login",bg = "white")
login_window.set_full_screen()
login_window.hide()

menu_window = Window(app, title="Menu",bg = "white")
menu_window.set_full_screen()
menu_window.hide()
add_med_window = Window(app, title="Add Medicine Window",bg = "white")
add_med_window.set_full_screen()
add_med_window.hide()
quit_med_window = Window(app, title="Quit Medicine Window",bg = "white")
quit_med_window.set_full_screen()
quit_med_window.hide()
check_pre_window = Window(app, title="Check Prescription Window",bg = "white")
check_pre_window.set_full_screen()
check_pre_window.hide()
emergency_window = Window(app, title="Emergency Window",bg = "white")
emergency_window.set_full_screen()
emergency_window.hide()
code_window = Window(app, title="Code",bg = "white")
code_window.set_full_screen()
code_window.hide()

welcome_text = Text(app,text="Welcome to use Smart Medbox, please login to proceed")
login_button = PushButton(app, command=open_window_login, text="Login")
ask_name_text = Text(login_window, text="Please type in your username")
ask_password_text = Text(login_window, text="Please type in your password")
my_name = TextBox(login_window)
my_password = TextBox(login_window)
submit_button = PushButton(login_window, text="Submit",command=submit)
back_button1 = PushButton(login_window, text="Back", command=back_window_login)


add_med_button = PushButton(menu_window, command=open_window1, text="Add Medicine")
ask_med_text = Text(add_med_window, text="Please type in your medicine name")
med_name = TextBox(add_med_window)
next_button = PushButton(add_med_window,text="Next",command=save_data)
back_button1 = PushButton(add_med_window, text="Back", command=back_window1)

quit_med_button = PushButton(menu_window, command=open_window2, text="Quit Medicine")
back_button2 = PushButton(quit_med_window, text="Back", command=back_window2)
check_pre = PushButton(menu_window, command=open_window3, text="Check Prescription")
back_button3 = PushButton(check_pre_window, text="Back", command=back_window3)
emergency = PushButton(menu_window, command=open_window4, text="Emergency call")
back_button4 = PushButton(emergency_window, text="Back", command=back_window4)
add_caregiver_code = PushButton(menu_window, command=open_window5, text="Caregiver Code")
medbox_id = Text(code_window, text="Your medbox id is: 1")
caregiver_code = Text(code_window, text=f"Your caregiver code is: {random_code}")
back_button5 = PushButton(code_window, text="Back", command=back_window5)

app.display()