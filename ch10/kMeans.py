from numpy import *
from urllib.request import urlopen 
from urllib import parse
import json
from time import sleep

def loadDataSet(fileName):
    fr = open(fileName)
    rowData = fr.readlines()
    length = len(rowData)
    dataMat = zeros((length,2))
    index = 0
    for line in rowData:
        curLine = line.strip().split('\t')
        dataMat[index,:] = curLine
        index += 1
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j])
        rangeJ = float(max(dataSet[:,j]) - minJ)
        centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
    return centroids

def kMeans(dataSet, k, distMeas = distEclud, creatCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroids = creatCent(dataSet,k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist= inf; minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j,:], dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j
            if clusterAssment[i,0] != minIndex: clusterChanged = True
            clusterAssment[i,:] = minIndex, minDist**2
        # print( centroids)
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A == cent)[0]]
            centroids[cent,:] = mean(ptsInClust, axis = 0)
    return centroids, clusterAssment

def biKmeans(dataSet,k,distMeas=distEclud):
    m = shape(dataSet)[0]
    # 将所有的点看成是一个簇
    # clusterAssment 存储 （所属的中心编号，距中心的距离）的列表
    clusterAssment = mat(zeros((m,2)))
    # centList 存储聚类中心
    centroid0 = mean(dataSet,axis=0).tolist()[0]
    centList = [centroid0]
    for j in range(m):
        clusterAssment[j,1] = distMeas(mat(centroid0),dataSet[j,:]) ** 2
    # 当簇小于数目k时
    while len(centList) < k:
        lowestSSE = inf
        for i in range(len(centList)):
            # 得到dataSet中行号与clusterAssment中所属的中心编号为i的行号对应的子集数据。
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]
            # 在给定的簇上进行K-均值聚类,k值为2
            centroidMat,splitClustAss = kMeans(ptsInCurrCluster,2,distMeas)
           # 计算将该簇划分成两个簇后总误差
            sseSplit = sum(splitClustAss[:,1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0],1])
            print("sseSplit, and not Split:", sseSplit, sseNotSplit)
           # 选择使得误差最小的那个簇进行划分
            if sseSplit + sseNotSplit < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat.copy()
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit

       # 将需要分割的聚类中心下的点进行1划分
       # 新增的聚类中心编号为len(centList)
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        print('the bestCentToSplit is:', bestCentToSplit)
        print('the len of bestClustAss is:', len(bestClustAss))
        
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] = bestClustAss

        # 更新被分割的聚类中心的坐标
        centList[bestCentToSplit] = bestNewCents[0,:]
       # 增加聚类中心
        centList.append(bestNewCents[1,:])

    return centList,clusterAssment

def geoGrab(stAddress, city):
    apiStem = 'http://where.yahooapis.com/geocode?'
    params = {}
    params['flags'] = 'J'
    params['appid'] = 'y8a56J3c'
    params['location'] = '%s %s' % (stAddress, city)
    url_params = parse.urlencode(params)
    yahooApi = apiStem + url_params
    print(yahooApi)
    c = urlopen(yahooApi)
    return json.loads(c.read())

if __name__ == '__main__':
    #dataMat = loadDataSet('testSet.txt')
    
    # print(randCent(dataMat, 3))
    
    # print(distEclud(dataMat[0], dataMat[1]))
    #kMeans(dataMat, 4)
    # print(kMeans(dataMat, 4))

    # dataMat3 = loadDataSet('testSet2.txt')
    # centList, myNewAssment = biKmeans(dataMat3,3)
    # print(centList)

    a = geoGrab('sh','sh')
    print(a)
