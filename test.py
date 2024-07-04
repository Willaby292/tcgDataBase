myDict = {}

idList = [1, 2, 1, 3]

for id in idList:
    if id in myDict:
        myDict[id].append('O')
    else:
        myDict[id] = ['X']

print(myDict)


def func1(data, **kwargs):
    # Function 1 logic here
    print("Function 1 called with data:", data)
    print("Function 1 called with kwargs:", kwargs)

def func2(data, **kwargs):
    # Function 2 logic here
    print("Function 2 called with data:", data)
    print("Function 2 called with kwargs:", kwargs)

    # Call func1 with the same positional and keyword arguments
    additional_kwarg = 'new_value'
    func1(data, additional_kwarg=additional_kwarg, **kwargs)

# Example usage
func2("example_data", collectible=1, pageSize=3)