from Subcom15_PsudoSub import communicate

testRuns = 1
testType = 3
randomType = 'R'
totalDaughterCommands = communicate(testRuns, "Daughter", testType, randomType)
print(f"Daughter's Total number of commands: {len(totalDaughterCommands)}")
print(f"Sent | Received")
print(totalDaughterCommands)