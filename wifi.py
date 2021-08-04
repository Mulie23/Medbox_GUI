import subprocess
import os

"""
NOTE : for the program to work , you need to have network-manager installed in the linux machine
TODO : to install network-manager run - 
     sudo apt install network-manager 

"""
class WIFI : 
    def __init__(self) : 
        self.data = {}

    def scan(self) : 
        self.data = {} 
        devices = subprocess.check_output(['netsh','wlan','show','network'])
        # decode it to strings
        devices = devices.decode('ascii')
        devices= devices.replace("\r","")
        print(devices)
        devices = devices.split("\n\n")

        for i in devices[1:-1] : 
            temp = i.split("\n")
            name = temp[0].split(":")[-1].strip(" ")
            interface = temp[2].split(":")[-1].strip(" ")
            self.data[name] = interface 
    
    """
    @arguments
        name is from the data 
        password is from the GUI
        interface wifi.data[name]

    """
    
    def connect(self, name, password, interface) : 
        try:
            os.system("nmcli d wifi connect {} password {} iface {}".format(name,password,interface))
        except:
            raise
        else:
            return True

wifi = WIFI() 
wifi.scan() 
print(wifi.data)
# 15168877330
