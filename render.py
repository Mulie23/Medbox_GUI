from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window

def create_login_screen():
    def submit():
        menu_window = Window(app, title="Menu",bg = "white")
        # menu_window.set_full_screen()
        add_med_button = PushButton(menu_window, command="", text="Add Medicine")
    def back_window_login():
        login_window.destroy()
    login_window=Window(app,title="Login")
    # login_window.set_full_screen()
    ask_name_text = Text(login_window, text="Please type in your username")
    ask_password_text = Text(login_window, text="Please type in your password")
    my_name = TextBox(login_window)
    my_password = TextBox(login_window)
    submit_button = PushButton(login_window, text="Submit",command=submit)
    back_button1 = PushButton(login_window, text="Back", command=back_window_login)
    


app = App(title="Homepage")
# app.set_full_screen()

welcome_text = Text(app,text="Welcome to use Smart Medbox, please login to proceed")
login_button = PushButton(app,command = create_login_screen, text="Login")




app.display()