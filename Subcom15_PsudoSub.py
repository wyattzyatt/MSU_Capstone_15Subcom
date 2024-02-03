"""
Created on Wed Dec 27 15:14:43 2023

@author: team Subcom15 - Wyatt
"""

#from static_utilities import StaticUtilities
import matlab.engine

class Communicator:
    
    def __init__(self, name: str = "Communicator Object", CMD: str = "Default") -> None :
        self.name: str = name
        self.commands: dict = {CMD:bin(0)}
        self.received: str = ''
        self.sent: str = ''
        self.testSystem: float = 0.0
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
    
    def sendCommand(self, CMD): # Calls the Matlab Scripts that will send the command to the other sub
        if(self.commands.get(CMD)):
            self.sent = self.commands[CMD]
            
            self.received = ''
            eng = matlab.engine.start_matlab()
            x = 0
            while self.received == '':
                if x == 0:
                    self.received = eng.Subcom15_Communicate(float(int(self.sent,2)), self.testSystem)
                    x=1
                    print(f"{self.sent} queued to send...")
            print(f"{self.received} received")
        else:
            print(f"{CMD} is not a recognized command")
        eng.quit
        return
            
    
    def readCommand(self):
        received = self.received
        return received
    
    def attachTestSystem(self):
        self.testSystem = 1.0
        
    def detachTestSystem(self):
        self.testSystem = 0.0

# Testing
c = Communicator()
print(c.commandList())
print(c.commandCodes())
c.addCommand("Forward")
print(c.commandList())
print(c.commandCodes())
c.addCommand("Backward")
print(c.commandList())
print(c.commandCodes())
c.attachTestSystem()
c.sendCommand("Forward")