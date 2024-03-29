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
    for i in range(3): 
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
    for i in range(3): 
        sendCmd = "Command229"
        Time = time.time()
        netSend(communicator,sendCmd,True)
        csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
    return

def netSend(communicator,cmd,slow):
    delayTime = 4
    time.sleep(delayTime)
    communicator.sendCommand(cmd)
    time.sleep(delayTime)
    communicator.join()
    if slow:
        time.sleep(delayTime*2)
    return

def doubleInit(file,communicator,title,comNum,commandNum):
    if(title == "Daughter"):
        for i in range(3):
            receivedCmd = netReceive(communicator)
            TimeRec = time.time()
            
            sendCmd = "Command229"
            TimeSen = time.time()
            netSend(communicator,sendCmd,True)
            csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec)
            
    if(title == "Mother"):
        for i in range(3):            
            sendCmd = "Command229"
            TimeSen = time.time()
            netSend(communicator,sendCmd,True)
            
            receivedCmd = netReceive(communicator)
            TimeRec = time.time()
            csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec)
    
    return

def csvWrite(file,communicator,title,comNum,SorR,commandNum,cmd,Time):
    file.writerow([f"{title}{comNum}{SorR}",commandNum,cmd, communicator.commands.get(cmd), Time])
    return

def csvWriteL(file,communicator,title,comNum,commandNum,cmdSent,TimeSent,cmdRec,TimeRec):
    file.writerow([f"{title}{comNum}", commandNum, "Sent:", cmdSent, communicator.commands.get(cmdSent), TimeSent,"Rec:", cmdRec, communicator.commands.get(cmdRec), TimeRec])
    return

def limitTest(communicator, Random, Seed, Add, Remove):
    if(Random == 0 or Random == 'N'):
        communicator.addCommand(f"Command{Seed}")
        return
    elif(Random == 1 or Random == 'R'):
        random.seed(Seed)
    elif(Random == 2 or Random == 'R2'):
        random.seed(Seed*Seed)
    currCount = communicator.length()
    if(Add):
        # Add commands of Random values
        addCount = random.randint(6, 10)
        attempt = 1
        while communicator.length() < currCount + addCount:
            prevCount = communicator.length()
            communicator.addCommand(f"Command{random.randint(0, 1024)}")
            if(communicator.length() == prevCount & attempt > 24):
                break
            attempt = attempt + 1
    if(Remove):
        # Remove commands from random locations
        removeCommands = random.sample(communicator.commandList(None), random.randint(1,5))
        for cmd in removeCommands:
            communicator.removeCommand(cmd)
    return

def communicate(numCommunicators, title, testType, randomType):
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
                limitTest(communicator,randomType,seed,True,True)
            # Add one additional set of commands with Random values
            limitTest(communicator,randomType,seed,True,False)
            print(f"Finished Command Number Testing, Commands: {communicator.length()}")
            
            with open(f"data/{title}{comNum}Commands.csv", 'w', newline='') as csvfile2:
                file2 = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(communicator.length()):
                    file2.writerow([f"{title}{comNum}",communicator.commandList(i), communicator.commandCodes(i)])
                
            seed = 1
            for i in range(1,comNum+1): seed = seed * i
            random.seed(seed)
            # Send all commands in random order
            shuffledCommands = communicator.commandList(None)#random.sample(communicator.commandList(None), communicator.length())
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
                
                elif(testType == 3):
                    doubleInit(file,communicator,title,comNum,commandNum)
                    for i in range (256):
                        receivedCmd = netReceive(communicator)
                        TimeRec = time.time()
                        
                        sendCmd = shuffledCommands[i]
                        TimeSen = time.time()
                        netSend(communicator,sendCmd,False)
                        csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec)
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
                
                elif(testType == 3):
                    doubleInit(file,communicator,title,comNum,commandNum)
                    for i in range (256):
                        sendCmd = shuffledCommands[i]
                        TimeSen = time.time()
                        netSend(communicator,sendCmd,False)
                        
                        receivedCmd = netReceive(communicator)
                        TimeRec = time.time()
                        csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec)
                        commandNum = commandNum + 1      
    return totalCommands
