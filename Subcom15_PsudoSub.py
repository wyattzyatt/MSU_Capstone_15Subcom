"""
Created on Wed Dec 27 15:14:43 2023

@author: team Subcom15 - Wyatt
"""

#from static_utilities import StaticUtilities
import matlab.engine
import threading

class Communicator:
    
    def __init__(self, name: str = "Communicator Object", CMD: str = "Default") -> None :
        self.name: str = name
        self.commands: dict = {CMD:bin(0)}
        self.received: str = ''
        self.sent: str = ''
        self.testSystem: float = 0.0
        self.thread = threading.Thread(target=self.sendCommandEx)
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
            tempItems = self.commands.items()
            tempItems2 = {}
            for i in tempItems:
                tempItems2[i[0]] = int(i[1],2)
            sorted_dict = dict(sorted(tempItems2.items(), key=lambda item: item[1]))
            i = 0
            for j in sorted_dict.values():
                if (i < 255):

                    if (i != j):
                        self.commands[CMD] = bin(i)
                        print(f"{CMD} Added to index {self.commands[CMD]}")
                        return
                    i = i + 1
                else:
                    print(f"Maximum Number of commands reached: {i}")
                    return
            self.commands[CMD] = bin(i)
            print(f"{CMD} Added to index {self.commands[CMD]}")
            
    
    def removeCommand(self, CMD): # Removes a command
        if(self.commands.get(CMD)):
            del self.commands[CMD]
        else:
            print(f"{CMD} is not a removable command")
    
    def sendCommandEx(self): # Calls the Matlab Scripts that will send the command to the other sub  
        self.received = ''
        eng = matlab.engine.start_matlab()
        x = 0
        while self.received == '':
            if x == 0:
                self.received = eng.Subcom15_Communicate(self.sent, self.testSystem)
                x=1
                print(f"{self.sent} queued to send...")
            else:
                self.received = eng.Subcom15_Communicate('', self.testSystem)
        print(f"{self.received} received")
        eng.quit
        return
         
    def readCommand(self):
        received = self.received
        return received
    
    def sendCommand(self, CMD): # Calls the sendCommandEx function with a single thread instead of the main thread so as to not bog down the system
        if(self.commands.get(CMD)):
            self.sent = self.commands[CMD]
            self.thread.start()
        else:
            print(f"{CMD} is not a recognized command")
            return
    
    def join(self):
        self.thread.join()
        
    def attachTestSystem(self):
        self.testSystem = 1.0
        
    def detachTestSystem(self):
        self.testSystem = 0.0

# Testing
c = Communicator("Communicator Object","Up")

c.addCommand(f"Down")
c.addCommand(f"Forward")
c.addCommand(f"Backward")

c.removeCommand(f"Forward")

c.addCommand(f"Left")
c.addCommand(f"Right")
c.addCommand(f"Forward")

print(c.commandList())
print(c.commandCodes())
c.attachTestSystem()
c.sendCommand("Forward")

    