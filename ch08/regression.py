from numpy import *

def loadDataSet(fileName):
    numFeat = len(open(fileName).readline().split('\t')) - 1
    dataMat = []; labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat

def standRegres(xArr, yArr):
    xMat = mat(xArr); yMat = mat(yArr).T
    xTx = xMat.T * xMat
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I *(xMat.T * yMat)
    return ws

def lwlr(testPoint, xArr, yArr, k = 1.0):
    xMat = mat(xArr); yMat = mat(yArr).T
    m = shape(xMat)[0]
    weights = mat(eye(m))
    for j in range(m):
        diffMat = testPoint - xMat[j,:]
        weights[j,j] = exp(diffMat * diffMat.T / (-2.0 * k**2))
    xTx = xMat.T * (weights * xMat)
    if linalg.det(xTx) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = xTx.I * (xMat.T * (weights * yMat))
    return testPoint * ws 

def lwlrTest(testArr, xArr, yArr, k = 1.0):
    m = shape(testArr)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i]= lwlr(testArr[i], xArr, yArr, k)
    return yHat

def rssError(yArr, yHatArror):
    return ((yArr - yHatArror) ** 2).sum()

def ridgeRegres(xMat, yMat, lam=0.2):
    xTx = xMat.T * xMat 
    denom = xTx + eye(shape(xMat)[1]) * lam
    if linalg.det(denom) == 0.0:
        print("This matrix is singular, cannot do inverse")
        return
    ws = denom.I * (xMat.T * yMat)
    return ws 

def ridgeTest(xArr, yArr):
    xMat = mat(xArr); yMat = mat(yArr).T 
    yMean = mean(yMat,0)
    yMat = yMat - yMean 
    xMeans = mean(xMat, 0)
    xVar = var(xMat, 0)
    xMat = (xMat - xMeans) / xVar 
    numTestPts = 30 
    wMat = zeros ((numTestPts,shape(xMat)[1]))
    for i in range(numTestPts):
        ws = ridgeRegres(xMat, yMat, exp(i-10))
        wMat[i, :] = ws.T
    return wMat

def stageWise(xArr, yArr, eps=0.01, numIt = 100):
    xMat = mat(xArr); yMat=mat(yArr).T 
    yMean = mean(yMat,0)
    yMat = yMat - yMean 
    xMat = regularize(xMat)
    m,n = shape(xMat)
    returnMat = zeros((numIt,n))
    ws = zeros((n,1)); wsTest = ws.copy(); wsMax = ws.copy()
    for i in range(numIt):
        print(ws.T)
        lowestError = inf
        for j in range(n):
            for sign in [-1,1]:
                wsTest = ws.copy()
                wsTest[j] += eps * sign
                yTest = xMat * wsTest
                rssE = rssError(yMat.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
        ws = wsMax.copy()
        returnMat[i,:] = ws.T 
    return returnMat

def regularize(xMat):#regularize by columns
    inMat = xMat.copy()
    inMeans = mean(inMat,0)   #calc mean then subtract it off
    inVar = var(inMat,0)      #calc variance of Xi then divide by it
    inMat = (inMat - inMeans)/inVar
    return inMat

if __name__ == '__main__':
    xArr, yArr = loadDataSet('ex0.txt')
    # ws = standRegres(xArr, yArr)
    # xMat = mat(xArr)
    # yMat = mat(yArr)
    # yHat = xMat * ws 

    # import matplotlib.pyplot as plt 
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.scatter(xMat[:,1].flatten().A[0], yMat.T[:,0].flatten().A[0])
    # xCopy = xMat.copy()
    # xCopy.sort(0)
    # yHat = xCopy * ws 
    # ax.plot(xCopy[:,1], yHat)
    # plt.show()
    # print(corrcoef(yHat.T, yMat))

    # yHat = lwlrTest(xArr, xArr, yArr, 0.01)
    # xMat = mat(xArr) 
    # strInd = xMat[:,1].argsort(0)
    # xSort = xMat[strInd][:,0,:]
    # import matplotlib.pyplot as plt 
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(xSort[:,1],yHat[strInd])
    # ax.scatter(xMat[:,1].flatten().A[0], mat(yArr).T.flatten().A[0], s=2, c='red')
    # plt.show()

    #abX, abY = loadDataSet('abalone.txt')
    # yHat01 = lwlrTest(abX[0:99], abX[0:99], abY[0:99], 0.1)
    # yHat1 = lwlrTest(abX[0:99], abX[0:99], abY[0:99], 1)
    # yHat10 = lwlrTest(abX[0:99], abX[0:99], abY[0:99], 10)
    # print(rssError(abY[0:99],yHat01.T))
    # print(rssError(abY[0:99],yHat1.T))
    # print(rssError(abY[0:99],yHat10.T))
    
    # yHat01 = lwlrTest(abX[200:299], abX[0:99], abY[0:99], 0.1)
    # yHat1 = lwlrTest(abX[200:299], abX[0:99], abY[0:99], 1)
    # yHat10 = lwlrTest(abX[200:299], abX[0:99], abY[0:99], 10)
    # print(rssError(abY[200:299],yHat01.T))
    # print(rssError(abY[200:299],yHat1.T))
    # print(rssError(abY[200:299],yHat10.T))

    # ws = standRegres(abX[0:99], abY[0:99])
    # yHat = mat(abX[200:299]) * ws
    # print(rssError(abY[200:299],yHat.T.A))

    # ridgeWeights = ridgeTest(abX, abY)
    # import matplotlib.pyplot as plt 
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(ridgeWeights[0:2])
    # plt.show()
    
    xArr, yArr = loadDataSet('abalone.txt')
    stageWise(xArr, yArr, 0.005, 1000)