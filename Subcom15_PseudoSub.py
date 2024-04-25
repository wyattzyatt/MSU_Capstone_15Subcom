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
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def receiveInit(file,communicator,title,comNum,commandNum):
    for i in range(3): 
        # Receive
        receivedData = netReceive(communicator)
        receivedCmd = receivedData[0]
        Time = receivedData[1]
        
        # Write Data to CSV
        csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
    return

def netReceive(communicator):
    attempt = 0
    receivedCmd = ''
    receivedCmd = communicator.readCommand()
    # Wait for Command
    while receivedCmd == '':
        time.sleep(0.01)
        attempt = attempt + 1
        if attempt > 1000:
            receivedCmd = communicator.readCommand()
    receivedData = [receivedCmd,time.time()]
    time.sleep(1.3) # Time for the Alternate system to start polling again
    return receivedData

def sendInit(file,communicator,title,comNum,commandNum,messageLength):
    for i in range(3): 
        # Send
        sendCmd = "Command229"
        Time = netSend(communicator,sendCmd,messageLength)
        
        # Write Data to CSV
        csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,Time)
    return

def netSend(communicator,cmd,messageLength):
    TimeSen = time.time()
    communicator.sendCommand(cmd)
    communicator.join()
    time.sleep(messageLength+0.1)
    return TimeSen

def doubleInit(file,communicator,title,comNum,commandNum,addedCommands,removedCommands,netCommands,messageLength):
    if(title == "Daughter"):
        for i in range(3):
            # Receive
            receivedData = netReceive(communicator)
            receivedCmd = receivedData[0]
            TimeRec = receivedData[1]
            
            # Send
            sendCmd = "Command229"
            TimeSen = netSend(communicator,sendCmd,messageLength)
            
            # Write Data to CSV
            csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec,addedCommands,removedCommands,netCommands,messageLength)
            
    if(title == "Mother"):
        for i in range(3):         
            # Send   
            sendCmd = "Command229"
            TimeSen = netSend(communicator,sendCmd,messageLength)
            
            # Receive
            receivedData = netReceive(communicator)
            receivedCmd = receivedData[0]
            TimeRec = receivedData[1]
            
            # Write Data to CSV
            csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec,addedCommands,removedCommands,netCommands,messageLength)
    
    return

# Write Data to CSV
def csvWrite(file,communicator,title,comNum,SorR,commandNum,cmd,Time):
    file.writerow([f"{title}{comNum}{SorR}",commandNum,cmd, communicator.commands.get(cmd), Time])
    return

# Write Data to CSV
def csvWriteL(file,communicator,title,comNum,commandNum,cmdSent,TimeSent,cmdRec,TimeRec,addedCommands,removedCommands,netCommands,messageLength):
    file.writerow([f"{title}{comNum}",addedCommands,removedCommands,netCommands, commandNum, "Sent:", cmdSent, communicator.commands.get(cmdSent), TimeSent,"Rec:", cmdRec, communicator.commands.get(cmdRec), TimeRec,"Message Length:",messageLength])
    # | Communicator Type | Commands Added | Commands Removed | Net Commands | commandNumber | Sent: | cmd | command binary | send Time | Received: | cmd | cmd binary | received Time | Message Length: | Message Length |
    return

# Test Limits of Adding and Removing from the communicator 
def limitTest(communicator, Random, Seed, Add, Remove):
    if(Random == 0 or Random == 'N'):
        communicator.addCommand(f"Command{Seed}")
        addCount = 1
        removeCommands = []
        commandsTested = [addCount, len(removeCommands)]
        return commandsTested
    elif(Random == 1 or Random == 'R'):
        random.seed(Seed)
    elif(Random == 2 or Random == 'R2'):
        random.seed(Seed*Seed)
    elif(Random == 3 or Random == 'R3'):
        Seed2 = 1
        for i in range(1,Seed): Seed2 = Seed2 * i
        random.seed(Seed2)
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
    removeCommands = []
    if(Remove):
        # Remove commands from random locations
        removeCommands = random.sample(communicator.commandList(None), random.randint(1,5))
        for cmd in removeCommands:
            communicator.removeCommand(cmd)
    commandsTested = [addCount, len(removeCommands)]
    return commandsTested

def communicate(numCommunicators, title, testType):
    # Attempt to make the data directory for storage
    currTime = f"{time.localtime()[3]%12}.{time.localtime()[4]}.{time.localtime()[5]}"
    currDate = f"{time.localtime()[1]}.{time.localtime()[2]}.{time.localtime()[0]}"
    try: os.mkdir(f"data/{currDate}")
    except: pass
    time.sleep(1)
    with open(f"data/{currDate}/{title}_{currTime}.csv", 'w', newline='') as csvfile:
        file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        # Input Number of Commands to Test per test (q) to quit
        inp = input(f"\nNumber of commands per test: ")
        commandTestCount = 256
        if inp == 'q' or inp == 'Q':
            print(f"{inp} pressed: Exiting")
            return
        elif float (inp):
            print(f"Number of commands to be tested per test: {inp}")
            commandTestCount = int (inp)
        
        if(title == "Mother"):
            # Initialize lists to store transmission times and running average
            transmission_times = []
            running_average = []

            # Initialize plot
            plt.ion()  # Turn on interactive mode
            fig, ax = plt.subplots()
            line, = ax.plot([], [], label='Transmission Time')
            avg_line, = ax.plot([], [], linestyle='--', color='green', label='Running Average')
            ax.legend()
            ax.set_title('Transmission Times and Running Average')
            ax.set_xlabel('Transmission Count')
            ax.set_ylabel('Time (s)')
            ax.grid(True)
        
        # Iterate through number of tests
        for comNum in range(numCommunicators):
            # Instantiate Communicator Object
            communicator = Communicator(f"{title} {comNum}",f"Command0")
            
            # Input Message Length for Test (q) to quit
            inp = input(f"\nTest {comNum} Message Length: ")
            messageLength = float(1)
            if inp == 'q' or inp == 'Q':
                print(f"{inp} pressed: Exiting")
                return
            elif float (inp):
                print(f"Message Length of {inp} Seconds")
                messageLength = float (inp)
                communicator.setMessageLength(messageLength)
        
            # Input randomization type to Test (q) to quit
            inp = input(f"\nTest {comNum} Randomization Type (N, R, R2, R3): ")
            if inp == 'q' or inp == 'Q':
                print(f"{inp} pressed: Exiting")
                return
            else:
                print(f"Random Type: {inp}")
                randomType = inp
                
            seed = 1
            commandsTested = [0,0]
            for seed in range (256):
                # Add sets of commands with Randomized values
                tempCommandsTested = limitTest(communicator,randomType,seed,True,True)
                commandsTested[0] = commandsTested[0] + tempCommandsTested[0]
                commandsTested[1] = commandsTested[1] + tempCommandsTested[1]
            # Add one additional set of commands with Random values
            tempCommandsTested = limitTest(communicator,randomType,seed,True,False)
            commandsTested[0] = commandsTested[0] + tempCommandsTested[0]
            commandsTested[1] = commandsTested[1] + tempCommandsTested[1]
            addedCommands =  commandsTested[0]
            removedCommands = commandsTested[1]
            netCommands = communicator.length()
            print(f"\nFinished Command Number Testing, Add Count, Remove Count, Net Commands: {commandsTested[0],commandsTested[1],netCommands}")
            
            # Record Commands to CSV for testing
            with open(f"data/{title}{comNum}Commands.csv", 'w', newline='') as csvfile2:
                file2 = csv.writer(csvfile2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(communicator.length()):
                    file2.writerow([f"{title}{comNum}",communicator.commandList(i), communicator.commandCodes(i)])
                
            # Send all commands in random order
            seed = 1
            for i in range(1,comNum+1): seed = seed * i
            random.seed(seed)
            shuffledCommands = communicator.commandList(None)#random.sample(communicator.commandList(None), communicator.length())
            commandNum = 0
            
            # Title of Mother or Daughter Decides communication order/functionality
            if(title == "Daughter"):
                # Only Receive
                if(testType == 1):
                    receiveInit(file,communicator,title,comNum,commandNum)
                    for i in range (commandTestCount):
                        # Receive
                        receivedData = netReceive(communicator)
                        receivedCmd = receivedData[0]
                        Time = receivedData[1]
                        
                        # Write Data to CSV
                        csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
                        commandNum = commandNum + 1
                        
                # Only Send
                elif(testType == 2):
                    sendInit(file,communicator,title,comNum,commandNum,messageLength)
                    for i in range (commandTestCount):
                        # Send
                        sendCmd = shuffledCommands[i]
                        TimeSen = netSend(communicator,sendCmd,messageLength)
                        
                        # Write Data to CSV
                        csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,TimeSen)
                        commandNum = commandNum + 1
                
                # Receive then Send
                elif(testType == 3):
                    doubleInit(file,communicator,title,comNum,commandNum,addedCommands,removedCommands,netCommands,messageLength)
                    startTime = time.time()
                    for i in range (commandTestCount):
                        # Receive
                        receivedData = netReceive(communicator)
                        receivedCmd = receivedData[0]
                        TimeRec = receivedData[1]
                        
                        print(f"Bidirectional transmission time: {TimeRec - startTime}")
                        
                        # Send
                        sendCmd = shuffledCommands[i]
                        TimeSen = netSend(communicator,sendCmd,messageLength)
                        
                        # Write Data to CSV
                        startTime = TimeSen
                        csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec,addedCommands,removedCommands,communicator.length(),messageLength)
                        commandNum = commandNum + 1

            elif(title == "Mother"):
                # Only Send
                if(testType == 1):
                    sendInit(file,communicator,title,comNum,commandNum,messageLength)
                    for i in range (commandTestCount):
                        # Send
                        sendCmd = shuffledCommands[i]
                        TimeSen = netSend(communicator,sendCmd,messageLength)
                        
                        # Write Data to CSV
                        csvWrite(file,communicator,title,comNum,"Sen:",commandNum,sendCmd,TimeSen)
                        commandNum = commandNum + 1
                
                # Only Receive
                elif(testType == 2):
                    receiveInit(file,communicator,title,comNum,commandNum)
                    for i in range (commandTestCount):
                        # Receive
                        receivedData = netReceive(communicator)
                        receivedCmd = receivedData[0]
                        TimeRec = receivedData[1]
                        
                        # Write Data to CSV
                        csvWrite(file,communicator,title,comNum,"Rec:",commandNum,receivedCmd,Time)
                        commandNum = commandNum + 1
                
                # Send Then Receive
                elif(testType == 3):
                    doubleInit(file,communicator,title,comNum,commandNum,addedCommands,removedCommands,netCommands,messageLength)
                    for i in range (commandTestCount):
                        # Send
                        sendCmd = shuffledCommands[i]
                        TimeSen = netSend(communicator,sendCmd,messageLength)
                        
                        # Receive
                        receivedData = netReceive(communicator)
                        receivedCmd = receivedData[0]
                        TimeRec = receivedData[1]
                        
                        # Calculate transmission time
                        transmission_time = TimeRec - TimeSen - 0.5
                        
                        # Append transmission time to the list
                        transmission_times.append(transmission_time)
                        
                        avgDepth = 10
                        dispDepth = 100
                        
                        # Update running average
                        avg = np.mean(transmission_times[-avgDepth:])
                        running_average.append(avg)
                        
                        # Update plot data
                        line.set_data(range(len(transmission_times[-dispDepth:])), transmission_times[-dispDepth:])
                        avg_line.set_data(range(len(running_average[-dispDepth:])), running_average[-dispDepth:])
                        
                        # Adjust plot limits
                        ax.set_xlim(0, len(transmission_times[-dispDepth:]))
                        ax.set_ylim(0, max(max(transmission_times[-dispDepth:]), max(running_average[-avgDepth:])) * 1.1)
                        
                        # Redraw plot
                        plt.draw()
                        plt.pause(0.001)
                        
                        # Write Data to CSV
                        csvWriteL(file,communicator,title,comNum,commandNum,sendCmd,TimeSen,receivedCmd,TimeRec,addedCommands,removedCommands,communicator.length(),messageLength)
                        commandNum = commandNum + 1
                        print(f"Bidirectional transmission time: {transmission_time}")
                        # plt.ioff()  # Turn off interactive mode after loop
                        plt.show()  # Keep plot open after loop ends
            file.writerow([])
            file.writerow([])
            file.writerow([])
            file.writerow([])
    return 
