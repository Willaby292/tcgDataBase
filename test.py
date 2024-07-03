myDict = {}

idList = [1, 2, 1, 3]

for id in idList:
    if id in myDict:
        myDict[id].append('O')
    else:
        myDict[id] = ['X']

print(myDict)