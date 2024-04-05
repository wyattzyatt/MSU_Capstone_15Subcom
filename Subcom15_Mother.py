from Subcom15_PsudoSub import communicate

testRuns = 10
testType = 3
randomType = 'N'
totalMotherCommands = communicate(testRuns, "Mother", testType, randomType)
print(f"Mother's Total number of commands: {len(totalMotherCommands)}")
print(f"Sent | Received")
print(totalMotherCommands)