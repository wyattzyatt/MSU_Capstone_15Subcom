# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 15:14:43 2023

@author: team Subcom15 - Wyatt
"""

#from static_utilities import StaticUtilities
import matlab.engine

class Communicator:
    
    def __init__(self, name: str = "Communicator Object", CMD: str = "Default") -> None:
        self.name: str = name
        self.commands: dict = {CMD:bin(0)}
        self.received: str = ""
        self.sent: str = ""
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
        self.commands[CMD] = bin(len(self.commands))
    
    def removeCommand(self, CMD): # Removes a command
        if(self.commands.get(CMD)):
            del self.commands[CMD]
    
    def sendCommand(self, CMD): # Calls the Matlab Scripts that will send the command to the other sub
        self.sent = self.commands[CMD]
        self.received = ""
        
        while self.received == "":
            self.received = self.eng.x(self.sent);
        return self.received
    
    def readCommand(self):
        received = self.received
        return received

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
c.removeCommand("Forward")
print(c.commandList())
print(c.commandCodes())