import guizero
# print(guizero.__version__)

from guizero import App, PushButton, Text

def update():
    return True

def tryit():
    while update != True:
        print("wait")
app = App(title="Hello World")

# app.set_full_screen()
text1 = Text(app, text="")
button1 = PushButton(app,text="Press me",command=update)
button2 = PushButton(app,text="Press me",command=tryit)

app.display()

