import subprocess
import os

"""
NOTE : for the program to work , you need to have network-manager installed in the linux machine
TODO : to install network-manager run - 
     sudo apt install network-manager 

"""
class WIFI : 
    def __init__(self) :
        pass
        


    def scan_windows(self) : 
        self.dictData = {} 
        #devices = subprocess.check_output(['wlan','network'])
        # decode it to strings
        devices = devices.decode('ascii')
        devices= devices.replace("\r","")
        devices = devices.split("\n\n")

        for i in devices[1:-1] : 
            temp = i.split("\n")
            name = temp[0].split(":")[-1].strip(" ")
            interface = temp[2].split(":")[-1].strip(" ")
            self.dictData[name] = interface 
    
    """
    @arguments
        name is from the data 
        password is from the GUI
        interface wifi.data[name]

    """
    
    def scan(self) :
        devices = os.popen("nmcli device wifi list").read()
        devices.replace("\r", " ")
        devices = devices.split("\n")
        data = set() 
        for i in devices[1:-1] :
            temp = i.split("\n")
            name = temp[0].replace("  "," ").split(" ")[4]
            data.add(name)
        return list(data)
           
        
    
    def connect(self, name, password = None, interface=None) : 
        try:
            base = "nmcli d wifi connect {}".format(name)
            if password!=None :
                base += " password {}".format(password)
            if interface!=None :
                base += " iface {}".format(interface)
            os.system(base) 
        except:
            raise
        else:
            return True

wifi = WIFI()
print(wifi.scan())
print(wifi.connect("WT", "15168877330"))
    
