from Subcom15_PsudoSub import communicate

testRuns = 1
testType = 1
totalMotherCommands = communicate(testRuns, "Test", testType)
print(f"Mother's Total number of commands: {len(totalMotherCommands)}")
print(f"Sent | Received")
print(totalMotherCommands)