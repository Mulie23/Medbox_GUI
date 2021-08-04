from guizero import App, Combo, Text, CheckBox, ButtonGroup, PushButton, info, TextBox, Picture, Slider, Window, info, Box
app = App(title="My second GUI app")
list1 = ["asd","asdaads","asasdasd"]
if len(list1)<10:
    for i in range(10-len(list1)):
        list1.append("")
combo1 = Combo(app, options=[list1[0],list1[1],list1[2],list1[3]])
app.display()
