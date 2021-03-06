import matplotlib.pyplot as plt

decisionNode = dict(boxstyle = "sawtooth", fc = "0.8")
leafNode = dict(boxStyle = "round4", fc = "0.8")
arrow_args = dict(arrowStyle = "<-")
xOff = 0
yOff = 0

def getNumLeafs(myTree):
    numLeafs = 0 
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":
            numLeafs += getNumLeafs(secondDict[key])
        else: numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0 
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == "dict":
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else: thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees =[{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
        {'no surfacing': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no' }}]
    return listOfTrees[i]

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy = parentPt, xycoords = 'axes fraction',\
        xytext = centerPt, textcoords = 'axes fraction', \
        va = "center", ha = "center", bbox = nodeType, arrowprops = arrow_args)

def plotTree(myTree, parentPt, nodeTxt):
    global xOff
    global yOff
    numLeafs = getNumLeafs(myTree)
    #depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    yOff = yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else: 
            xOff = xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (xOff, yOff), \
                cntrPt, leafNode)
            plotMidText((xOff, yOff), cntrPt, str(key))
    yOff = yOff + 1.0 / plotTree.totalD

def createPlot(inTree):
    global xOff
    global yOff
    fig = plt.figure(1, facecolor ='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon = False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    xOff = -0.5 / plotTree.totalW; yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()

def  classify(inputTree , featLabels, testVec):
    filterStr = list(inputTree.keys())[0]
    secondDict = inputTree[filterStr]
    featIndex = featLabels.index(filterStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else: classLabel = secondDict[key]
    return classLabel

if __name__ == '__main__':
    myTree = retrieveTree(0)
    labels = ['no surfacing', 'flippers']
    print(createPlot(myTree))
    print(classify(myTree, labels, [1,1]))