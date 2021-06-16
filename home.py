from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window

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
    f=open('D:/Term 8/Capstone/medbox_data.txt','w')
    f.write(my_name.value+'\n')
    f.close
    
app = App(title="Homepage",layout="grid", width=476, height=208)

add_med_window = Window(app, title="Add Medicine Window",layout="grid")
add_med_window.hide()
quit_med_window = Window(app, title="Quit Medicine Window")
quit_med_window.hide()
check_pre_window = Window(app, title="Check Prescription Window")
check_pre_window.hide()
emergency_window = Window(app, title="Emergency Window")
emergency_window.hide()

add_med_button = PushButton(app, command=open_window1, text="Add Medicine", grid=[0,0], width=30, height=5)
ask_med_text = Text(add_med_window, text="Please type in your medicine name", grid=[0,0])
my_name = TextBox(add_med_window,grid=[1,0])
next_button = PushButton(add_med_window,text="Next",command=save_data,grid=[0,1])
close_button1 = PushButton(add_med_window, text="Close", command=close_window1,grid=[1,1])

quit_med_button = PushButton(app, command=open_window2, text="Quit Medicine", grid=[0,1], width=30, height=5)
close_button2 = PushButton(quit_med_window, text="Close", command=close_window2)
check_pre = PushButton(app, command=open_window3, text="Check Prescription", grid=[1,0], width=30, height=5)
close_button3 = PushButton(check_pre_window, text="Close", command=close_window3)
emergency = PushButton(app, command=open_window4, text="Emergency call", grid=[1,1], width=30, height=5)
close_button4 = PushButton(emergency_window, text="Close", command=close_window4)

app.display()