from Subcom15_PsudoSub import communicate

testRuns = 10
testType = 3
randomType = 'N'
totalDaughterCommands = communicate(testRuns, "Daughter", testType, randomType)
print(f"Daughter's Total number of commands: {len(totalDaughterCommands)}")
print(f"Sent | Received")
print(totalDaughterCommands)