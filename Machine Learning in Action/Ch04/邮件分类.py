from numpy import*

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
        #else:   print("the word: {} is not in my Vocabulary".format(word))
    return returnVec

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):  #预测，使用朴素贝叶斯
    log_p1 = sum(vec2Classify * p1Vec) + log(pClass1)      #对概率取了对数
    log_p0 = sum(vec2Classify * p0Vec) + log(1.0-pClass1)  #对概率取了对数
    if log_p1 > log_p0:
        return 1
    else:
        return 0

def trainNB0(trainMatrix,labelsVec):  #训练函数,计算概率
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

'''
def textParse(bigString): #使用正则表示式表示句子
    import re
    #listOfTokens = re.split(r'\\w*',bigString)
    #regEx = re.compile(r'\\w*')
    regEx = re.compile(r'[!@#$%^&*()? \n~/]') #使用正则化指定划分的字符
    listOfTokens = regEx.split(bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]
'''

def textParse(bigString): 
    import re
    listOfTokens = re.split(r'[!@#$%^&*()? \n~/]',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]



def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1,26):
        path = 'E:\机器学习实战\Ch04\email\spam\%d.txt' % i
        wordList = textParse(open(path).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        path = 'E:\机器学习实战\Ch04\email\ham\%d.txt' % i
        wordList = textParse(open(path).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)  #创造词组，用共有的单词建立词组，用于预测
    print(vocabList)
    trainingSet = list(range(50))  #0-49 变成list
    testSet = []
    for i in range(10):  #划分训练集，测试集
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex]) #一定要用del
    trainMat = []
    trainClasses = []
    for docIndex in trainingSet:  #获得训练集
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        #print(wordVector)
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
            #print(docList[docIndex],docIndex)
    print("the error rate is: {}".format(float(errorCount)/len(testSet)))


spamTest()












