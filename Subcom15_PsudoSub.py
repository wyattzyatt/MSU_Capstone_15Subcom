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

def receiveInit(file,communicator,title,comNum,commandNum):
    receivedCmd = netReceive(communicator)
    Time = time.time()
    csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
    receivedCmd = netReceive(communicator)
    Time = time.time()
    csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
    receivedCmd = netReceive(communicator)
    Time = time.time()
    csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
    return

def netReceive(communicator):
    attempt = 0
    receivedCmd = ''
    receivedCmd = communicator.readCommand()
    while receivedCmd == '':
        time.sleep(0.01)
        attempt = attempt + 1
        if attempt > 1000:
            receivedCmd = communicator.readCommand()
    return receivedCmd

def sendInit(file,communicator,title,comNum,commandNum):
    sendCmd = "Command229"
    Time = time.time()
    netSend(communicator,sendCmd,True)
    csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
    Time = time.time()
    netSend(communicator,sendCmd,True)
    csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
    Time = time.time()
    netSend(communicator,sendCmd,True)
    csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
    return

def netSend(communicator,cmd,slow):
    delayTime = 2
    communicator.sendCommand(cmd)
    time.sleep(delayTime)
    communicator.join()
    if slow:
        time.sleep(delayTime*2)
    return

def csvWrite(file,communicator,title,comNum,SorR,commandNum,cmd,Time):
    file.writerow([f"{title}{comNum}{SorR}",commandNum,cmd, communicator.commands.get(cmd), Time])
    return

def limitTest(communicator, random, seed, Add, Remove):
    if(random == 0):
        communicator.addCommand(f"Command{seed}")
        return
    elif(random == 1):
        random.seed(seed)
    elif(random == 2):
        random.seed(seed*seed)
    currCount = len(communicator.commandList())
    if(Add):
        # Add commands of Random values
        addCount = random.randint(6, 10)
        attempt = 1
        while len(communicator.commandList()) < currCount + addCount:
            prevCount = len(communicator.commandList())
            communicator.addCommand(f"Command{random.randint(0, 1024)}")
            if(len(communicator.commandList()) == prevCount & attempt > 24):
                break
            attempt = attempt + 1
    if(Remove):
        # Remove commands from random locations
        removeCommands = random.sample(communicator.commandList(), random.randint(1,5))
        for cmd in removeCommands:
            communicator.removeCommand(cmd)
    return
        
        

def communicate(numCommunicators, title, testType):
    totalCommands = list( None for _ in range(numCommunicators*256))
    
    currTime = f"{time.localtime()[3]%12}.{time.localtime()[4]}.{time.localtime()[5]}"
    currDate = f"{time.localtime()[1]}.{time.localtime()[2]}.{time.localtime()[0]}"
    try: os.mkdir(f"data/{currDate}")
    except: pass
    time.sleep(1)
    with open(f"data/{currDate}/{title}_{currTime}.csv", 'w', newline='') as csvfile:
        file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for comNum in range(numCommunicators):
            communicator = Communicator(f"{title} {comNum}",f"Command0")
            seed = 1
            for seed in range (256):
                limitTest(communicator,0,seed,True,True)
            # Add one additional set of commands with Random values
            limitTest(communicator,0,seed,True,False)
            print(f"Finished Command Number Testing, Commands: {len(communicator.commandList())}")
            
            seed = 1
            for i in range(1,comNum+1): seed = seed * i
            random.seed(seed)
            # Send all commands in random order
            shuffledCommands = communicator.commandList()#random.sample(communicator.commandList(), len(communicator.commandList()))
            commandNum = 0
                            
            if(title == "Daughter"):
                if(testType == 1):
                    receiveInit(file,communicator,title,comNum,commandNum)
                    for i in range (256):
                        receivedCmd = netReceive(communicator)
                        Time = time.time()
                        totalCommands[comNum*256 + commandNum] = [receivedCmd, communicator.commands.get(receivedCmd), Time]
                        csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
                        commandNum = commandNum + 1
                        
                elif(testType == 2):
                    sendInit(file,communicator,title,comNum,commandNum)
                    for sendCmd in shuffledCommands:
                        Time = time.time()
                        netSend(communicator,sendCmd,False)
                        totalCommands[comNum*256 + commandNum] = [sendCmd, communicator.commands.get(sendCmd), Time]
                        csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
                        commandNum = commandNum + 1

            elif(title == "Mother"):
                if(testType == 1):
                    sendInit(file,communicator,title,comNum,commandNum)
                    for sendCmd in shuffledCommands:
                        Time = time.time()
                        netSend(communicator,sendCmd,False)
                        totalCommands[comNum*256 + commandNum] = [sendCmd, communicator.commands.get(sendCmd), Time]
                        csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
                        commandNum = commandNum + 1
                
                elif(testType == 2):
                    receiveInit(file,communicator,title,comNum,commandNum)
                    for i in range (256):
                        receivedCmd = netReceive(communicator)
                        Time = time.time()
                        totalCommands[comNum*256 + commandNum] = [receivedCmd, communicator.commands.get(receivedCmd), Time]
                        csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
                        commandNum = commandNum + 1
    return totalCommands
