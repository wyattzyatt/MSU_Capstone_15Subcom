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
    my_communicator.attachmessageLength()
    my_communicator.detachmessageLength()
Join Threads (if necessary):
    my_communicator.join()

--------------------------
"""
#from static_utilities import StaticUtilities
import matlab.engine
import threading
import time
from pytictoc import TicToc

class Communicator:
    
    def __init__(self, name: str = "Communicator Object", CMD: str = "Default") -> None :
        self.name: str = name
        self.commands: dict = {CMD:bin(0)}
        self.received: str = ''
        self.receivedBin = []
        self.send: str = ''
        self.sendBin = []
        self.messageLength: float = 0.7
        self.timer1 = TicToc()
        self.timer1.tic()
        self.eng = matlab.engine.start_matlab()
        self.timer1.toc("matlab eng took")
        print(f"{self.name} initialized")
        #StaticUtilities.logger.info(f"{self.name} initialized")
    
    def getName(self):
        Name = self.name
        return Name

    def commandList(self, index): # Returns the list if commands the communicator currently has
        nlist = list(self.commands.keys())
        if index != None:
            return nlist[index]
        else:
            return nlist
    
    def commandCodes(self, index): # Returns the codes for the commands that the communicator currently has
        nlist = list(self.commands.values())
        if index != None:
            return nlist[index]
        else:
            return nlist
    
    def length(self):
        length = len(self.commands)
        return length
    
    def addCommand(self, CMD): # Adds a command to the Communicator's repertoire
        if(self.commands.get(CMD)):
            return 0
            #print(f"{CMD} is already a command")
        else:
            commandListBin = self.commands.items() # Sorts the binary values in the dictionary
            commandListInts = {}
            for i in commandListBin:
                commandListInts[i[0]] = int(i[1],2)
            sorted_dict = dict(sorted(commandListInts.items(), key=lambda item: item[1]))
            i = 0
            for j in sorted_dict.values(): # Iterates through the sorted values to find the index to put the next comand
                if (i < 255):
                    if (i != j):
                        self.commands[CMD] = bin(i)
                        return 1
                    i = i + 1
                else:
                    #print(f"Maximum Number of commands reached: {i + 1}")
                    return 0
            self.commands[CMD] = bin(i)
            return 1
            
    
    def removeCommand(self, CMD): # Removes a command from anywhere in the command list
        if(self.commands.get(CMD)):
            del self.commands[CMD]
            return 1
        else:
            print(f"{CMD} is not a removable command")
            return 0
        return
    
    def sendCommandEx(self): # Sends the command that is queued in self.send or to read from the communicator
        if (self.send != ''):
            pySendCommand = [float(int(c)) for c in self.sendBin[2:len(self.send)].zfill(8)] # creates an array of matlab formatted values from the binary
            self.eng.Subcom15_Communicate(pySendCommand, self.messageLength)
            time.sleep(1)
            self.send = ''
            self.sendBin = []
            return
        self.receivedBin = []
        while self.receivedBin == []:
            self.receivedBin = self.eng.Subcom15_Communicate('', self.messageLength)[0]
        return
         
    def readCommand(self): # Returns the currently received command
        received = ''
        if(self.receivedBin != []):
            binConversion = bin(int("".join(str(x)[0] for x in self.receivedBin), 2)) # Converts the received matlab format into a python binary string
            for cmd in self.commands.keys():
                if(self.commands.get(cmd) == binConversion):
                    self.received = cmd
                    received = self.received
                    self.receivedBin = []
        else:
            self.send = ''
            self.thread = threading.Thread(target=self.sendCommandEx)
            self.thread.start()
            while self.receivedBin == []:
                pass
            binConversion = bin(int("".join(str(x)[0] for x in self.receivedBin), 2)) # Converts the received matlab format into a python binary string
            for cmd in self.commands.keys():
                if(self.commands.get(cmd) == binConversion):
                    self.received = cmd
                    received = self.received
                    self.receivedBin = []
           # print(f"Command Hasn't Been Received Yet")
        return received
            
    
    def sendCommand(self, CMD): # Calls the sendCommandEx function with a single thread instead of the main thread so as to not bog down the system
        if(self.commands.get(CMD)):
            self.send = CMD
            self.sendBin = self.commands[CMD]
            self.thread = threading.Thread(target=self.sendCommandEx)
            self.thread.start()
            return 1
        else:
            print(f"{CMD} is not a recognized command")
            return 0
        return
    
    def setSendCommand(self, CMD): # Allows setting the send command for Explicit command sending 
        if(self.commands.get(CMD)):
            self.send = CMD
            self.sendBin = self.commands[CMD]
            return 1
        else:
            print(f"{CMD} is not a recognized command")
            return 0
        return
    
    def join(self): # If using the default command sending join threads once done to return threads to be usable
        try: self.thread.join()
        except: pass
        return
        
    def setMessageLength(self,newMessageLength: float = 0.7): # Attaches the Test System for displaying information through MATLAB
        if newMessageLength > 0:
            self.messageLength = newMessageLength
            return 1
        else:
            self.messageLength = 0.7 # Default message length
            return 0