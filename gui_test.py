import guizero
# print(guizero.__version__)

from guizero import App, PushButton, Text

credit = False

def update():
    return True

def tryit():
    global credit
    credit = True


app = App(title="Hello World")

# app.set_full_screen()
text1 = Text(app, text="")
button1 = PushButton(app,text="Press me",command=update)
button2 = PushButton(app,text="Press me",command=tryit)

app.display()

