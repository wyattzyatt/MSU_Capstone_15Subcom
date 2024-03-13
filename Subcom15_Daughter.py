from Subcom15_PsudoSub import communicate

testRuns = 1
testType = 1
totalDaughterCommands = communicate(testRuns, "Daughter", testType)
print(f"Daughter's Total number of commands: {len(totalDaughterCommands)}")
print(f"Sent | Received")
print(totalDaughterCommands)