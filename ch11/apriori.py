def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))

#该函数用于从 C1 生成 L1 。
def scanD(D,Ck,minSupport):
#参数：数据集、候选项集列表 Ck以及感兴趣项集的最小支持度 minSupport
    ssCnt={}
    for tid in D:#遍历数据集
        for can in Ck:#遍历候选项
            if can.issubset(tid):#判断候选项中是否含数据集的各项
                #if not ssCnt.has_key(can): # python3 can not support
                if not can in ssCnt:
                    ssCnt[can]=1 #不含设为1
                else: ssCnt[can]+=1#有则计数加1
    numItems=float(len(D))#数据集大小
    retList = []#L1初始化
    supportData = {}#记录候选项中各个数据的支持度
    for key in ssCnt:
        support = ssCnt[key]/numItems#计算支持度
        if support >= minSupport:
            retList.insert(0,key)#满足条件加入L1中
        supportData[key] = support
    return retList, supportData

def aprioriGen(LK, k): #creates Ck
    retList = []
    lenLK = len(LK)
    for i in range(lenLK):
        for j in range(i+1, lenLK):
            L1 = list(LK[i])[:k-2]; L2 = list(LK[j])[:k-2]
            L1.sort(); L2.sort()
            if L1 == L2:
                retList.append(LK[i] | LK[j])
    return retList

def apriori(dataSet, minSupport = 0.5):
    C1 = createC1(dataSet)
    D = list(map(set,dataSet))
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1 
    return L, supportData

def generateRules(L, supportData, minConf = 0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList

def calcConf(freqSet, H, supportData, brl, minConf = 0.7):
    prunedH = []
    for conseq in H: 
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print (freqSet - conseq, '-->', conseq, 'conf:', conf)
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf = 0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):
        Hmp1 = aprioriGen(H, m + 1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)

if __name__ == '__main__':
    dataSet = loadDataSet()
    
    # C1 = createC1(dataSet)
    # D = list(map(set,dataSet))
    # L1, suppData0 = scanD(D, C1, 0.5)
    
    # L, suppData = apriori(dataSet, minSupport=0.5)
    # rules = generateRules(L, suppData, minConf = 0.7)

    mushDataSet = [line.split() for line in open('mushroom.dat')]
    L, suppData = apriori(mushDataSet, minSupport=0.3)
    for item in L[1]:
        if item.intersection('2'): print (item)

