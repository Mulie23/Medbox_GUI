import guizero
# print(guizero.__version__)

from guizero import App, PushButton, Text

def update():
    text1.value = 1
app = App(title="Hello World")

# app.set_full_screen()
text1 = Text(app, text="")
button1 = PushButton(app,text="Press me",command=update)

app.display()