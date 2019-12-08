from numpy import*
import matplotlib.pyplot as plt

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0,float(lineArr[0]),float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat,labelMat

def sigmoid(intX):
    return 1.0/(1 + exp(-intX))

def gradAscent(dataMat,classLabel):  #梯度上升
    dataMatrix = mat(dataMat)
    labelMat = mat(classLabel).transpose()  #对矩阵转置
    m,n = shape(dataMatrix)
    alpha = 0.001   #学习率
    maxCycles = 500 #迭代次数
    weights = ones((n,1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix*weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error  #注意推导
    return weights

def stocGradAscent0(dataMat,classLabel,numIter=150):  #随机梯度上升
    m,n = shape(dataMat)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0 +j + i) + 0.01  #调整alpha
            randIndex = int(random.uniform(0,len(dataIndex))) # 随机选取更新
            h = sigmoid(sum(dataMat[randIndex]*weights))
            error = (classLabel[randIndex] - h)
            weights = weights + alpha * error * dataMat[randIndex]
            del (dataIndex[randIndex])
    return weights

def classifyVector(intX,weights):
    prob = sigmoid(sum(intX*weights))
    #print(prob)
    if prob > 0.5:
        return 1.0
    else:
        return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainingSet = []
    trainingLabels = []
    for line in frTrain.readlines():
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        trainingSet.append(lineArr)
        trainingLabels.append(float(currLine[21]))
    trainWeights = stocGradAscent0(array(trainingSet),trainingLabels,500)
    #trainWeights = gradAscent(trainingSet,trainingLabels)
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines(): #小心
        numTestVec += 1.0
        currLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(currLine[i]))
        if int(classifyVector(array(lineArr),trainWeights)) != int(float(currLine[21])):
                errorCount += 1
    errorRate = (float(errorCount)/numTestVec)
    print("the error rate of this test is: %f" % errorRate)
    return errorRate

def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print("after %d iterations the average error rate is:%f"%(numTests,errorSum/float(numTests)))

'''
def plotBestFit(wei):
    #weights = wei.getA() #?  #将矩阵wei转化为list
    weights = array(wei)
    dataMat,labelMat = loadDataSet()
    dataArr = array(dataMat)
    n = shape(dataArr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArr[i,1])
            ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1])
            ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green')
    x = arange(-3.0,3.0,0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel("X1")
    plt.ylabel("Y1")
    plt.show()
'''

multiTest()
