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

def testCommunicators(numCommunicators):
    for comNum in range(numCommunicators):
        communicator = Communicator(f"Test Communicator {comNum}",f"Command0")
        numCommands = 1
        while numCommands <= 255:
            # Generate a random number of commands to add and remove
            addCount = random.randint(5, 10)
            removeCount = random.randint(1,5)
            
            # Add commands
            for i in range(addCount):
                if numCommands <= 255:
                    communicator.addCommand(f"Command{numCommands}")
                    numCommands += 1
            
            # Remove commands from random locations
            removeCommands = random.sample(communicator.commandList(), removeCount)
            for cmd in removeCommands:
                if numCommands < 255:
                    communicator.removeCommand(cmd)
                    numCommands -= 1
                
            if numCommands > 255:
                print(f"Communicator {comNum} reached maximum commands: {numCommands}")
                # Send all commands in random order
                shuffledCommands = random.sample(communicator.commandList(), len(communicator.commandList()))
                print(f"Shuffled commands: {shuffledCommands}")
                for cmd in shuffledCommands:
                    communicator.sendCommand(cmd)
                    while communicator.readCommand() == '':
                        time.sleep(0.01)
                    communicator.join()
                break
                
            
# Testing
# TotalSentCommands = [][]
testCommunicators(100)

# communicator = Communicator(f"Test Communicator {0}",f"Command0")

# numCommands = 1
# while numCommands <= 255:
#     communicator.addCommand(f"Command{numCommands}")
#     numCommands += 1

# random_command = random.choice(communicator.commandList())
# communicator.setSendCommand(random_command)
# communicator.sendCommandEx()
# time.sleep(1)   
# read = communicator.readCommand()
# time.sleep(1)
# communicator.join()

# Look into multiprocessing toolbox