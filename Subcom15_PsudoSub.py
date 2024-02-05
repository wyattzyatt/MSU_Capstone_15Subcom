"""
--------------------------
15Subcom Capstone Project
Communication Protocol Testing
@author: team SubCom15 - Wyatt
Created on Wed Dec 27 15:14:43 2023
--------------------------
"""
from Subcom15_Communicator import Communicator
# Testing
c = Communicator("Communicator Object","Up")

c.addCommand(f"Down")
c.addCommand(f"Forward")
c.addCommand(f"Backward")

c.removeCommand(f"Forward")

c.addCommand(f"Left")
c.addCommand(f"Right")
c.addCommand(f"Forward")

print(c.commandList())
print(c.commandCodes())
c.attachTestSystem()
c.sendCommand("Forward")

    