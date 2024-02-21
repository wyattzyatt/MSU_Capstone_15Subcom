"""
--------------------------
15Subcom Capstone Project
Communication Protocol
@author: team SubCom15 - Wyatt
Created on Wed Dec 27 15:14:43 2023
--------------------------
The Communicator class facilitates communication between systems by sending and receiving commands. 
It allows for adding, removing, and executing commands, as well as attaching and detaching a test system. 
The class employs multithreading to send commands without blocking the main thread.

Use Case:

my_communicator = Communicator(name="My Communicator", CMD="Default")

Add Commands:
    my_communicator.addCommand("NewCommand")
Remove Commands:
    my_communicator.removeCommand("NewCommand")
Send Commands:
    my_communicator.sendCommand("NewCommand")
Set Send Commands:
    my_communicator.sendCommand("NewCommand")
Read Received Command:
    received_command = my_communicator.readCommand()
Attach/Detach Test System:
    my_communicator.attachTestSystem()
    my_communicator.detachTestSystem()
Join Threads (if necessary):
    my_communicator.join()

--------------------------
"""
#from static_utilities import StaticUtilities
import matlab.engine
import threading
from multiprocessing import Process

class Communicator:
    
    def __init__(self, name: str = "Communicator Object", CMD: str = "Default") -> None :
        self.name: str = name
        self.commands: dict = {CMD:bin(0)}
        self.received: str = ''
        self.receivedBin = []
        self.send: str = ''
        self.sendBin = []
        self.testSystem: float = 0.0
        self.eng = matlab.engine.start_matlab()
        print(f"{self.name} initialized")
        #StaticUtilities.logger.info(f"{self.name} initialized")
    
    def commandList(self): # Returns the list if commands the communicator currently has
        nlist = self.commands.keys()
        return list(nlist)
    
    def commandCodes(self): # Returns the codes for the commands that the communicator currently has
        nlist = self.commands.values()
        return list(nlist)
    
    def addCommand(self, CMD): # Adds a command to the Communicator's repertoire
        if(self.commands.get(CMD)):
            print(f"{CMD} is already a command")
        else:
            tempItems = self.commands.items() # Sorts the binary values in the dictionary
            tempItems2 = {}
            for i in tempItems:
                tempItems2[i[0]] = int(i[1],2)
            sorted_dict = dict(sorted(tempItems2.items(), key=lambda item: item[1]))
            i = 0
            for j in sorted_dict.values(): # Iterates through the sorted values to find the index to put the next comand
                if (i < 255):
                    if (i != j):
                        self.commands[CMD] = bin(i)
                        print(f"{CMD} Added to index {self.commands[CMD]}") # Adds the command to the index found
                        return
                    i = i + 1
                else:
                    print(f"Maximum Number of commands reached: {i}")
                    return
            self.commands[CMD] = bin(i)
            print(f"{CMD} Added to index {self.commands[CMD]}")
            return
            
    
    def removeCommand(self, CMD): # Removes a command from anywhere in the command list
        if(self.commands.get(CMD)):
            print(f"removing {CMD} from {self.commands[CMD]}")
            del self.commands[CMD]
        else:
            print(f"{CMD} is not a removable command")
        return
    
    def sendCommandEx(self): # Sends the command that is queued in self.send or to read from the communicator
        if (self.send != ''):
            pySendCommand = [float(int(c)) for c in self.sendBin[2:len(self.send)].zfill(8)]
            print(f"Communicator Sending: {self.send, self.sendBin, pySendCommand}")
            self.eng.Subcom15_Communicate(pySendCommand, self.testSystem)
            self.send = ''
            self.sendBin = []
        self.receivedBin = []
        while self.receivedBin == []:
            self.receivedBin = self.eng.Subcom15_Communicate('', self.testSystem)[0]
        print(f"Communicator Received {self.receivedBin}")
        return
         
    def readCommand(self): # Returns the currently received command
        for cmd in self.commands.keys():
            if(self.commands.get(cmd) == self.receivedBin):
                print(f"{cmd}")
        received = self.received
        return received
    
    def sendCommand(self, CMD): # Calls the sendCommandEx function with a single thread instead of the main thread so as to not bog down the system
        if(self.commands.get(CMD)):
            self.send = CMD
            self.sendBin = self.commands[CMD]
            self.thread = threading.Thread(target=self.sendCommandEx)
            self.thread.start()
        else:
            print(f"{CMD} is not a recognized command")
        return
    
    def setSendCommand(self, CMD): # Allows setting the send command for Explicit command sending 
        if(self.commands.get(CMD)):
            self.send = CMD
            self.sendBin = self.commands[CMD]
        else:
            print(f"{CMD} is not a recognized command")
        return
    
    def join(self): # If using the default command sending join threads once done to return threads to be usable
        self.thread.join()
        return
        
    def attachTestSystem(self): # Attaches the Test System for displaying information through MATLAB
        self.testSystem = 1.0
        return
        
    def detachTestSystem(self): # Detaches the Test System
        self.testSystem = 0.0
        return
    
