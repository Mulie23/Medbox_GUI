import guizero
print(guizero.__version__)

from guizero import App

app = App(title="Hello World")

app.set_full_screen()

app.display()