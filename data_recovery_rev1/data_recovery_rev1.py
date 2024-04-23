
import code
from concurrent.futures import thread
from socket import timeout
import tkinter as tk
from tkinter import *
import sys
import os
import ctypes
import threading

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
 # Re-run the script as an administrator
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

def start_thread():
    # global stop_recovery
    # if stop_recovery:
    #     print("Stopped .")
    # else: 
    #     thread = threading.Thread(target=start_recovery)
    #     thread.start()
    global stop_recovery 
    stop_recovery = False
    global thread
    thread = threading.Thread(target=start_recovery)
    thread.start()

def stop_thread():  
    global stop_recovery
    global thread
    stop_recovery = True
    
    thread.join(timeout = 1)


def start_recovery():

        global stop_recovery
         # drive = "\\\\.\\D:"     # Open drive as raw bytes
        drive = "\\\\.\\"+clicked.get()
        fileD = open(drive, "rb")
        size = 512              # Size of bytes to read
        byte = fileD.read(size) # Read 'size' bytes
        offs = 0                # Offset location
        drec = False            # Recovery mode
        rcvd = 0                # Recovered file ID

        while byte:
            
            if stop_recovery:
                text_box.insert("end", os.linesep+"Recovery Stopped. Succesfully recovered "+str(rcvd)+" JPGs."+os.linesep)
                break

            found = byte.find(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46')
            if found >= 0:
                    drec = True
                    text_box.insert("end", '==== Found JPG at location: ' + str(hex(found+(size*offs))) + ' ====\n')
                    # Now lets create recovered file and search for ending signature
                    fileN = open(str(rcvd) + '.jpg', "wb")
                    fileN.write(byte[found:])
                    while drec:
                    
                        byte = fileD.read(size)
                        bfind = byte.find(b'\xff\xd9')
                        if bfind >= 0:
                            fileN.write(byte[:bfind+2])
                            fileD.seek((offs+1)*size)
                            text_box.insert("end", '==== Wrote JPG to location: ' + str(rcvd) + '.jpg ====\n')
                            drec = False
                            rcvd += 1
                            fileN.close()
                        else:
                            fileN.write(byte)
            byte = fileD.read(size)
            offs += 1
        fileD.close()
           
        
def stop_recovery():
    global stop_recovery
    stop_recovery = True

root = tk.Tk()
root.geometry("400x600")
root.title("Pictures Recovery by FRLNCEDEV")
p1 = PhotoImage(file = 'frlncedev_logo.png')
  
# Setting icon of master window
root.iconphoto(False, p1)

# Dropdown menu options
options = [
    "A:",
    "B:",
    "C:",
    "D:",
    "E:",
    "F:",
    "G:",
    "H:",
    "I:", "I:", "J:","K:"
]
  
stop_recovery = False
# datatype of menu text
clicked = StringVar()
  
# initial menu text
clicked.set( "C:" )

# Create Dropdown menu
drop = OptionMenu( root , clicked , *options )
drop.pack()


text_box = tk.Text(root)
text_box.pack(expand=True, fill="both")

# create a scrollbar
scrollbar = tk.Scrollbar(text_box)
scrollbar.pack(side="right", fill="y")

# associate the scrollbar with the text box
text_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_box.yview)

start_button = tk.Button(root, text="Start Recovery", command=start_thread)
start_button.pack()

stop_button = tk.Button(root, text="Stop Recovery", command=stop_thread)
stop_button.pack()

root.mainloop()

