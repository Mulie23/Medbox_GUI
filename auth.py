from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window
import requests 
import json
import base64
import random
import string
random_code =  ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
def open_window1():
    login_window.show(wait=True)
def close_window1():
    login_window.hide()
def submit():
    body =  {'username': my_name.value , 'password' : my_password.value }
    response = requests.post('http://3.0.17.207:4000/medboxAuth/login', body)
    data = response.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    print(data)
    # if data["success"] == 1:
    #     menu_window.show(wait=True)
    #     body = {'code':caregiver_code.value,'jwt':data['success']['jwt']}
    #     response2 = requests.post('http://3.0.17.207:4000/medboxAuth/login', body)
    menu_window.show(wait=True)
app = App(title="Homepage",layout="grid")
login_window = Window(app, title="Login",layout="grid")
login_window.hide()
menu_window = Window(app, title="Menu",layout="grid")
menu_window.hide()

add_med_button = PushButton(app, command=open_window1, text="Login", grid=[0,0], width=30, height=5)
ask_name_text = Text(login_window, text="Please type in your username", grid=[0,0])
ask_password_text = Text(login_window, text="Please type in your password", grid=[0,1])
my_name = TextBox(login_window,grid=[1,0])
my_password = TextBox(login_window,grid=[1,1])
submit_button = PushButton(login_window, text="Submit",command=submit, grid=[0,2])
close_button1 = PushButton(login_window, text="Close", command=close_window1,grid=[1,2])
caregiver_code = Text(menu_window, text=f"Your caregiver code is {random_code}", grid=[0,0])

app.display()