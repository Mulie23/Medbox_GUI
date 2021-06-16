from guizero import App, Window, PushButton

def open_window():
    window.show(wait=True)

def close_window():
    window.hide()

app = App(title="Main window")

window = Window(app, title="Second window")
window.hide()

open_button = PushButton(app, text="Open", command=open_window)
close_button = PushButton(window, text="Close", command=close_window)

app.display()
