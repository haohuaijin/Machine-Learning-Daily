import feedparser
from numpy import*

def textParse(bigString):  #分割文本
    import re
    listOfTokens = re.split(r'["-_''><=+:;.@#$%^&*()? \n~/]',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

#创造单词的列表
def createVocabList(dataSet):
    vocabSet = set([])
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

#词袋模型
def bagOfWords2Vec(vocabList,inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):  #预测，使用朴素贝叶斯
    log_p1 = sum(vec2Classify * p1Vec) + log(pClass1)      #对概率取了对数
    log_p0 = sum(vec2Classify * p0Vec) + log(1.0-pClass1)  #对概率取了对数
    if log_p1 > log_p0:
        return 1
    else:
        return 0

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

def calcMostFreq(vocabList,fullText):  #统计词频
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFreq = sorted(freqDict.items(),key=operator.itemgetter(1),reverse=True)
    return sortedFreq[:30]

def localWords(feed1,feed0):
    docList = []
    classList = []
    fullText = []
    minLen = min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen): #导入RSS源
        wordList = textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    top30Words = calcMostFreq(vocabList,fullText)
    for pariw in top30Words: #top30words为元组类型
        if pariw[0] in vocabList:
            vocabList.remove(pariw[0])
    #print(minLen)
    trainingSet = list(range(2*minLen))  #转换为list型
    testSet = []
    for i in range(int(0.3*minLen)):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(bagOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for i in testSet:
        wordVector = bagOfWords2Vec(vocabList,docList[i])
        #print(wordVector)
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[i]:
            errorCount += 1
    print("the error rate is: {}".format(float(errorCount)/len(testSet)))
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V = localWords(ny,sf)
    topNY = []
    topSF = []
    for i in range(len(p0V)):
        if p0V[i] > 0.5:   topSF.append((vocabList[i],p0V[i]))
        if p1V[i] > 0.5:   topNY.append((vocabList[i],p1V[i]))
    sortedSF = sorted(topSF,key=lambda x:x[1],reverse=True)
    print("SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**SF**")
    for item in sortedSF:
        print(item[0])
    sortedNY = sorted(topNY,key=lambda x:x[1],reverse=True)
    print("NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**NY**")
    for i in sortedNY:
        print(item[0])

ny = feedparser.parse('http://www.nasa.gov/rss/dyn/image_of_the_day.rss')
sf = feedparser.parse('http://www.cppblog.com/kevinlynx/category/6337.html/rss')
'''
ny = feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
sf = feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')
'''
getTopWords(ny,sf)


