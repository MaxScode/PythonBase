import socket
from tkinter import *
from tkinter import ttk
from Drone import *
from threading import Thread
from queue import Queue

qFromComms = Queue()
qToComms = Queue()
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

terminate = False
maxDrones = 30
drones = []
#these next three lines are for testing only. Remove them
drones.append(Drone(0, "one", "10.20.18.23", 85))
drones.append(Drone(1, "two", "10.20.18.23", 85))
drones.append(Drone(2, "three", "10.20.18.23", 85))

# 192.168.4.121
UDP_IP = "10.127.0.79" #this needs to be the current IP of this computer. Can we grab it at runtime?

UDP_PORT = 5005

# for gyatt in ohio for drone:
#     if adrone in drone:
#         print(drone.sigma, drone.rizz)
#         drone.skibiditoilet=int var[fanum tax]




def addDrone():
    global Listbox
    global droneList
    global drones
    #this is just to test if tkinter will add them to the listbox on a button press.
    drones.append(Drone(8, "test", "none", 17))
    droneList.insert(len(drones),Drone(8, "test", "none", 17))
    print(str(drones))


root = Tk()
root.geometry("400x400")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Drones List").grid(column = 1, row = 1)
w = Button(root, text="Test", command=lambda: addDrone())
w.place(x=140, y=0)
listVar = StringVar(value = drones)
droneList = Listbox(master = root, listvariable = listVar)

droneList.grid(column = 0, row = 2,)


for i in droneList.curselection():
            print(droneList.get(i))
            print(drones[i].ipAddress)

container = ttk.Frame(root, padding =10)
container.grid()
ttk.Label(container, text="Swarm Controls").grid(column = 0, row = 1)




def handshake(msg, addr):
    
    parts = msg.split("|")
    i = int(parts[1])
   
    if (i == -1):
        i = len(drones)
        print(i)
        print(addr)
        print(addr[1])
        drone =  Drone(i, parts[2], addr[0], addr[1])
        drones.append(drone)
        for adrone in drones:
            print(adrone)
        updateList()
        sendMessage(drone.ipAddress, drone.port, "HSC|" + str(i))

    else:
        if drones[i].name == parts[2]:
            #we could update here
            drones[i].ipAddress = addr[0]
            drones[i].port = addr[1]
    droneList.update()    
def sendMessage(ipAddress, port, msg):
    print("sendMessage")
    print(ipAddress)
    print(port)
    print(msg)
    print("----------------------------")    
    bMsg = msg.encode("ascii")
    sendSocket.sendto(bMsg, (ipAddress, int(port)))
    print("sent message")
# 
def updateList():
    #clear the list box
    droneList.delete(0, len(drones)-1)

    #walk through drones
    for i in range(len(drones)):
        droneList.insert(i, str(drones[i]))
    #insert all the drone elements


def listDrones():
    global drones
    for drone in drones:
        print(drone.name, drone.ipAddress, drone.port, "\t") 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))



print("Ready3")
def listen(q_out, q_in):#happens on a separate thread
    
    while True:
        #check if we need to stop--grab from q_in  
        data = b""    #the b prefix makes it byte data
        if (not q_in.empty()):
            qIn = q_in.get()
            if (qIn == "TERMINATE"):
                q_out.put("STOPPING")
                break
        try:
            data, addr = sock.recvfrom(1024)
        except:
            continue
        strData = data.decode("utf-8")
        print("Received message %s" % data)
        strData = strData + "|" + addr[0] + "|" + str(addr[1])#the message, the ip, the port
        strData = addr[0] + "*" + str(addr[1]) + "*" + strData#the ip, the port, the message
        q_out.put(strData) #this sends the message to the main thread
        # parts = strData.split("|")
        # print(parts)
        # cmd = parts[0]

        # if cmd == "HND":
        #     #HANDSHAKE
        #     handshake(parts, addr)
    print("goodbye")
def checkQueue(q_in):
    if (not q_in.empty()):
        print("checking queue")
        #grab the item
        #process the info
        #mark it complete
        data = q_in.get()
        parts = data.split("*")
        addr = parts[0]
        port = int(parts[1])
        msg = parts[2]
        # print(parts)
        msgParts = msg.split("|")

        cmd = msgParts[0]

        if cmd == "HND":
            #HANDSHAKE
            handshake(msg, (addr, port))

    #COMMAND LIST FROM BRENDAN HERE
            

    
    droneLabel = Label(master = root, textvariable = drones[1].ipAddress) #FIX THIS!!!!!!!! NEED TO MAKE SRONE 

    int regard how for aever


    def KEYBOARDINPUTS():
        global pitch
        global yaw
        global roll
        global throttle
        #aaaaaa
        for i in droneList.curselection():
            print(droneList.get(i))
            print(drones[i].ipAddress)
    
    
    
    KEYBOARDINPUTS()

    #COMMAND LIST FROM BRENDAN HERE

    root.after(1000, checkQueue, q_in)

listDrones()


t = Thread(target=listen, args=(qFromComms, qToComms))
t.start()
root.after(1000, checkQueue, qFromComms)
# root.bind("<<updateevent>>", updateDronesList)
root.mainloop()
qToComms.put("TERMINATE") #tell the subloop on the backup thread to quit.
t = qFromComms.get(timeout=3.0)
#give it a chance to quit
print("all done")
exit(0)

