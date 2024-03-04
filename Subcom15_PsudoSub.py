"""
--------------------------
15Subcom Capstone Project
Communication Protocol Testing
@author: team SubCom15 - Wyatt
Created on Fri Mar 1 2024
--------------------------
"""
from Subcom15_Communicator import Communicator
import random
import time
from pytictoc import TicToc

def communicate(numCommunicators, Title):
    totalCommands = list( None for _ in range(numCommunicators*256))
    for comNum in range(numCommunicators):
        communicator = Communicator(f"{Title} {comNum}",f"Command0")
        seed = 1
        for seed in range (256):
            random.seed(seed)
            currCount = len(communicator.commandList())
            
            # Add commands of Random values
            addCount = random.randint(6, 10)
            while len(communicator.commandList()) < currCount + addCount:
                communicator.addCommand(f"Command{random.randint(0, 1024)}")
            
            # Remove commands from random locations
            removeCommands = random.sample(communicator.commandList(), random.randint(1,5))
            for cmd in removeCommands:
                communicator.removeCommand(cmd)
        
        # Add one additional set of commands with Random values
        random.seed(seed)
        currCount = len(communicator.commandList())
        
        # Add commands of Random values
        addCount = random.randint(6, 10)
        while len(communicator.commandList()) < currCount + addCount:
            communicator.addCommand(f"Command{random.randint(0, 1024)}")
           
        seed = 1
        for i in range(1,comNum+1): seed = seed * i
        random.seed(seed)
        # Send all commands in random order
        shuffledCommands = random.sample(communicator.commandList(), len(communicator.commandList()))
        commandNum = 0
        for sendCmd in shuffledCommands:
            if(Title == "Daughter"):
                receivedCmd = communicator.readCommand()
                while receivedCmd == '':
                    time.sleep(0.01)
                    receivedCmd = communicator.readCommand()
                communicator.sendCommand(sendCmd)
                time.sleep(1)
            elif(Title == "Master"):
                communicator.sendCommand(sendCmd)
                time.sleep(1)
                receivedCmd = communicator.readCommand()
                while receivedCmd == '':
                    time.sleep(0.01)
                    receivedCmd = communicator.readCommand()
            totalCommands[comNum*256 + commandNum] = [sendCmd,receivedCmd]
            commandNum = commandNum + 1
            communicator.join()
    return totalCommands
        
# Testing
testRuns = 1
totalDaughterCommands = communicate(testRuns, "Daughter")
totalMasterCommands = communicate(testRuns, "Master")
print(f"Master's Total number of commands: {len(totalMasterCommands)}")
print(f"Sent | Received")
print(totalMasterCommands)

