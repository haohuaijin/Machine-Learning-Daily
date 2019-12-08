from numpy import*

#创造实验样本
def loadDataSet():
    postinfList = [['my','dog','has','flea','problems','help','please'],\
                   ['maybe','not','take','him','to','doy','park','stupid'],\
                   ['my','dalmation','is','so','cute','I','love','him'],\
                   ['stop','posting','stupid','worthless','garbage'],\
                   ['mr','licks','ate','my','steak','how','to','stop','him'],\
                   ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1]
    return postinfList,classVec

#创造单词的列表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

#词集模型
#统计单词是否出现
def setOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:   print("the word: {} is not in my Vocabulary".format(word))
    return returnVec

'''
#词袋模型
def bagOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec
'''

def trainNB0(trainMatrix,labelsVec):  #训练函数
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(labelsVec)/float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if labelsVec[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += 1
            #p1Denom += sum(trainMatrix[i])  #?为什么不是p1Denom += 1
        else:
            p0Num += trainMatrix[i]
            p0Denom += 1
            #p0Denom += sum(trainMatrix[i])  #?为什么不是p0Denom += 1
    #print(p1Num,p0Num)
    p1Vec = log(p1Num/p1Denom)
    p0Vec = log(p0Num/p0Denom)
    #print(p1Denom,p0Denom)
    return p0Vec,p1Vec,pAbusive

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):  #预测，使用朴素贝叶斯
    log_p1 = sum(vec2Classify * p1Vec) + log(pClass1)      #对概率取了对数
    log_p0 = sum(vec2Classify * p0Vec) + log(1.0-pClass1)  #对概率取了对数
    if log_p1 > log_p0:
        return 1
    else:
        return 0

def testinfNB():  #测试系统
    List,classVec = loadDataSet()
    vocabList = createVocabList(List)
    trainMat = []
    for i in List:
        trainMat.append(setOfWords2Vec(vocabList,i))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(classVec))
    testEntry = ['love','my','dalmation']
    thisDoc = array(setOfWords2Vec(vocabList,testEntry))
    print("{} class as: {}".format(testEntry,classifyNB(thisDoc,p0V,p1V,pAb)))
    testEntry = ['stupid','garbage']
    thisDoc = array(setOfWords2Vec(vocabList,testEntry))
    print("{} class as: {}".format(testEntry,classifyNB(thisDoc,p0V,p1V,pAb)))   


testinfNB()















