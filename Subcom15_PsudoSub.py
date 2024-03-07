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
import csv
import os

def communicate(numCommunicators, Title):
    totalCommands = list( None for _ in range(numCommunicators*256))
    for comNum in range(numCommunicators):
        communicator = Communicator(f"{Title} {comNum}",f"Command0")
        currTime = f"{time.localtime()[3]%12}.{time.localtime()[4]}.{time.localtime()[5]}"
        currDate = f"{time.localtime()[1]}.{time.localtime()[2]}.{time.localtime()[0]}"
        try: os.mkdir(f"data/{currDate}")
        except: pass
        with open(f"data/{currDate}/{Title}{comNum} {currTime}.csv", 'w', newline='') as csvfile:
            file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            seed = 1
            for seed in range (256):
                random.seed(seed)
                currCount = len(communicator.commandList())
                
                # Add commands of Random values
                addCount = random.randint(6, 10)
                attempt = 1
                while len(communicator.commandList()) < currCount + addCount:
                    prevCount = len(communicator.commandList())
                    communicator.addCommand(f"Command{random.randint(0, 1024)}")
                    if(len(communicator.commandList()) == prevCount & attempt > 24):
                        break
                    attempt = attempt + 1
                
                # Remove commands from random locations
                removeCommands = random.sample(communicator.commandList(), random.randint(1,5))
                for cmd in removeCommands:
                    communicator.removeCommand(cmd)
            
            # Add one additional set of commands with Random values
            random.seed(seed)
            currCount = len(communicator.commandList())
            
            # Add commands of Random values
            addCount = random.randint(6, 10)
            attempt = 1
            while len(communicator.commandList()) < currCount + addCount:
                prevCount = len(communicator.commandList())
                communicator.addCommand(f"Command{random.randint(0, 1024)}")
                if(len(communicator.commandList()) == prevCount & attempt > 24):
                    break
                attempt = attempt + 1
            print(f"Finished Command Number Testing, Commands: {len(communicator.commandList())}")
            
            seed = 1
            for i in range(1,comNum+1): seed = seed * i
            random.seed(seed)
            # Send all commands in random order
            shuffledCommands = random.sample(communicator.commandList(), len(communicator.commandList()))
            commandNum = 0
            timer1 = TicToc()
            timer2 = TicToc()
            for int in range(20):
                timer1.tic()
                timer2.tic()
                timer1.toc("Initializing Timer1: ")
                timer2.toc("Initializing Timer2: ")
                
            for sendCmd in shuffledCommands:
                if(Title == "Daughter"):
                    receivedCmd = communicator.readCommand()
                    while receivedCmd == '':
                        time.sleep(0.01)
                        receivedCmd = communicator.readCommand()
                    Time = timer1.tocvalue()
                    timer2.tic()
                    communicator.sendCommand(sendCmd)
                    time.sleep(1)
                elif(Title == "Master"):
                    timer1.tic()
                    communicator.sendCommand(sendCmd)
                    time.sleep(1)
                    receivedCmd = communicator.readCommand()
                    while receivedCmd == '':
                        time.sleep(0.01)
                        receivedCmd = communicator.readCommand()
                    Time = timer2.tocvalue()
                totalCommands[comNum*256 + commandNum] = [sendCmd,receivedCmd,Time]
                commandNum = commandNum + 1
                file.writerow([sendCmd, receivedCmd, Time])
                communicator.join()
    return totalCommands
        
# Testing
testRuns = 1
totalDaughterCommands = communicate(testRuns, "Daughter")
totalMasterCommands = communicate(testRuns, "Master")
print(f"Master's Total number of commands: {len(totalMasterCommands)}")
print(f"Sent | Received")
print(totalMasterCommands)
