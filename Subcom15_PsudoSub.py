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

def test_communicators(num_communicators):
    for _ in range(num_communicators):
        communicator = Communicator(f"Test Communicator {_}",f"Command0")
        num_commands = 1
        while num_commands <= 255:
            # Generate a random number of commands to add and remove
            num_to_add = random.randint(5, 10)
            num_to_remove = random.randint(1,5)
            
            # Add commands
            for i in range(num_to_add):
                if num_commands <= 255:
                    communicator.addCommand(f"Command{num_commands}")
                    num_commands += 1
            
            # Remove commands from random locations
            commands_to_remove = random.sample(communicator.commandList(), num_to_remove)
            for cmd in commands_to_remove:
                if num_commands < 255:
                    communicator.removeCommand(cmd)
                    num_commands -= 1
                
            if num_commands > 255:
                print(f"Communicator {_} reached maximum commands: {num_commands}")
                # Send all commands in random order
                shuffled_commands = random.sample(communicator.commandList(), len(communicator.commandList()))
                print(f"Shuffled commands: {shuffled_commands}")
                for cmd in shuffled_commands:
                    communicator.sendCommand(cmd)
                    while communicator.readCommand() == '':
                        time.sleep(0.01)
                    communicator.join()
                break
                
            # Ensure more commands are added than removed
            assert num_commands >= 0, "Number of commands cannot be negative"
            
# Testing
test_communicators(100)

# communicator = Communicator(f"Test Communicator {0}",f"Command0")

# num_commands = 1
# while num_commands <= 255:
#     communicator.addCommand(f"Command{num_commands}")
#     num_commands += 1

# random_command = random.choice(communicator.commandList())
# communicator.setSendCommand(random_command)
# communicator.sendCommandEx()
# time.sleep(1)   
# read = communicator.readCommand()
# time.sleep(1)
# communicator.join()

# Look into multiprocessing toolbox