import guizero
# print(guizero.__version__)

from guizero import App, PushButton, Text, Window
from threading import Timer
import time
isfinish = False
yesno_press = False
submit_quan_value = False

def confirm_finish():
    global submit_quan_value
    submit_quan = True
    quantity_window.hide()
    # scan_window.hide()
    confirm_finish_window.show()

def finish_yes_func():
    global isfinish
    global yesno_press
    yesno_press = True
    isfinish = True
    confirm_finish_window.hide()
    menu_window.show(wait=True)

def finish_no_func():
    global isfinish
    global yesno_press
    yesno_press = True
    isfinish = False
    confirm_finish_window.hide()
    quantity_window.show()

def check_choice():
    # global yesno_press
    # while yesno_press == False:
    #     confirm_finish_window.show(wait=True)
    return True



def check_submit_quan():
    # global submit_quan_value
    # while submit_quan_value == False:
    #     quantity_window.show(wait=True)
    return True

def refillProcess():

    # quantity_window.show(wait=True) 
    # pull updated prescription 
    global isfinish
    global yesno_press
    global submit_quan_value
    
    # container = Containers(DIR, STEP, SLEEP) 
    stateMachine = True ; 
    state = 'wait'
    def checkQuanState():
        if submit_quan_value == True:
            state = "ask"
            return True
        return False
    while(stateMachine) : 
        # if (state=="barcode") : 
            # display the relevant details on the front end - Wentao
            # scan_window.show(wait=True)
            # information on what medicine are to be filled up 
            # medicine_id = checkBarcode() ; 
            # if medicine_id!=None : 
                # state = "rotate"

            # add GUI interrupt 
        # elif (state=="rotate") : 
        #     container_id = container.getContainer(medicine_id)
        #     if container.rotateContainerToRefillArea() : 
        #         state="wait"
        #     else : 
        #         state = "error"
        #         message = "couldn't rotate container"
        if (state=="wait") : 
            quantity_window.show(wait=True)
            # scan_window.hide()
            # wait for a button push on gui and number of pills form input 
            # update infromation i.e container.json
            # if refillComplete() : 
            #     state = "finish"
            while True:
                timer = Timer(5, checkQuanState)
                timer.start()
                timer.join()
                if submit_quan_value== True:
                    break
                # else:
                #     state = "wait"
        elif (state=="ask") :   
            print("done") 
            stateMachine = False
        #     check_choice()                
        #     if isfinish==True : 
        #         state = "finish"
        #     else : 
        #         state = "wait" 
        # elif (state=="finish"): 
        #     # container.writeToFile() 
        #     stateMachine = False 
        # elif  (state=="error") : 
        #     error = "there was some error" 
        #     stateMachine = False 
        # else : 
        #     state = "error" 
        #     error = "invalid sate" 

    return  True    

def add_one():
    int_qun = int(quantity_no.value)
    int_qun += 1
    quantity_no.value =int_qun

def add_five():
    int_qun = int(quantity_no.value)
    int_qun += 5
    quantity_no.value =int_qun

def add_ten():
    int_qun = int(quantity_no.value)
    int_qun += 10
    quantity_no.value =int_qun

def minus_one():
    int_qun = int(quantity_no.value)
    int_qun -= 1
    quantity_no.value =int_qun

def minus_five():
    int_qun = int(quantity_no.value)
    int_qun -= 5
    quantity_no.value =int_qun

def minus_ten():
    int_qun = int(quantity_no.value)
    int_qun -= 10
    quantity_no.value =int_qun

def open_quan():
    quantity_window.show()
app = App(title="Hello World")
menu_window = Window(app,title="menu")
start_btn = PushButton(menu_window,text="start",command=open_quan)
# menu_window.hide()
quantity_window = Window(app, title="Quantity",bg = (255,255,224))
# quantity_window.set_full_screen()
quantity_no_info = Text(quantity_window,text="Please input the quantity of the medicine refilled")
quantity_no = Text(quantity_window,text="0")
minus_one_btn = PushButton(quantity_window, text ="-1", command=minus_one)
minus_five_btn = PushButton(quantity_window, text ="-5", command=minus_five)
minus_ten_btn = PushButton(quantity_window, text ="-10", command=minus_ten)
add_one_btn = PushButton(quantity_window, text ="+1", command=add_one)
add_five_btn = PushButton(quantity_window, text ="+5", command=add_five)
add_ten_btn = PushButton(quantity_window, text ="+10", command=add_ten)
submit_quan_btn = PushButton(quantity_window, text ="Submit", command=confirm_finish)
quantity_window.hide()

confirm_finish_window = Window(app, title="Confirm finish",bg = (255,255,224))
# confirm_finish_window.set_full_screen()
confirm_finish_window.hide()
confirm_finish_txt = Text(confirm_finish_window,text="Do you want to refill other medicines?")
finish_yes = PushButton(confirm_finish_window, text ="Yes", command=finish_yes_func)
finish_no = PushButton(confirm_finish_window, text ="No", command=finish_no_func)

app.display()

