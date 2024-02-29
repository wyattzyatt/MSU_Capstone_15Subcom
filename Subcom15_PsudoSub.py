"""
--------------------------
15Subcom Capstone Project
Communication Protocol Testing
@author: team SubCom15 - Wyatt
Created on Mon Feb 5 2024
--------------------------
"""
from Subcom15_Communicator import Communicator
import random
import time
from pytictoc import TicToc

def testCommunicators(numCommunicators):
    totalCommands = list( None for _ in range(numCommunicators*256))
    for comNum in range(numCommunicators):
        communicator = Communicator(f"Test Communicator {comNum}",f"Command0")
        while 1:
            # Generate a random number of commands to add and remove
            addCount = random.randint(5, 10)
            removeCount = random.randint(1,5)
            currCount = len(communicator.commandList())

            if currCount > 255:
                print(f"Communicator {comNum} reached maximum commands: {len(communicator.commandList())}")
                # Send all commands in random order
                shuffledCommands = random.sample(communicator.commandList(), len(communicator.commandList()))
                commandNum = 0
                for sendCmd in shuffledCommands:
                    communicator.sendCommand(sendCmd)
                    time.sleep(1)
                    receivedCmd = communicator.readCommand()
                    while receivedCmd == '':
                        time.sleep(0.01)
                        receivedCmd = communicator.readCommand()
                    totalCommands[comNum*256 + commandNum] = [sendCmd,receivedCmd]
                    commandNum = commandNum + 1
                    communicator.join()
                break
            else:
                # Add commands
                while len(communicator.commandList()) < currCount + addCount:
                    if len(communicator.commandList()) <= 255:
                        communicator.addCommand(f"Command{random.randint(0, 1024)}")
                    else:
                        break
                
                # Remove commands from random locations
                removeCommands = random.sample(communicator.commandList(), removeCount)
                for cmd in removeCommands:
                    if len(communicator.commandList()) < 255:
                        communicator.removeCommand(cmd)
    return totalCommands
                
            
# Testing
totalCommands = testCommunicators(1)
print(f"Total number of commands: {len(totalCommands)}")
print(f"Sent | Received")
print(totalCommands)
# communicator = Communicator(f"Test Communicator {0}",f"Command0")


# random_command = random.choice(communicator.commandList())
# communicator.setSendCommand(random_command)
# communicator.sendCommandEx()
# time.sleep(1)   
# read = communicator.readCommand()
# time.sleep(1)
# communicator.join()

# Look into multiprocessing toolbox