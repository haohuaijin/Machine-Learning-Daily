from numpy import *
import operator
import os

def classify0(inX,dataSet,labels,k):  #对向量进行分类
	#dataSetSize = dataSet.shape[0]               #行数
	#diffMat = tile(inX,(dataSetSize,1))-dataSet  #对向量进行复制，得到和dataSet一样的大小
	diffMat = inX-dataSet                         #利用广播更加简单
	sqDiffMat = diffMat**2                       #d对差值平方
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	sortedDistIndicies = distances.argsort()
	classCount = {}
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
	sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True)
	return sortedClassCount[0][0]

def img2vector(filename):   #读取文本，将他转换为(1,1024)的矩阵
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        Line = fr.readline()
        for j in range(32):
            returnVect[0,32*i + j] = eval(Line[j]) #通过readline读出来的是str需要取出来变为整型
    return returnVect

def handwritingClassTest():  #测试代码
    Labels = []
    trainingFileList = os.listdir('E:/机器学习实战/Ch02/trainingDigits')#用地址是为了避免'\0','\t'所以用/来分割地址
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        filestr = fileNameStr.split('.')[0]
        classNumStr = eval(filestr.split('_')[0])
        Labels.append(classNumStr)
        trainingMat[i,:] = img2vector('E:/机器学习实战/Ch02/trainingDigits/' + fileNameStr)
    testFileList =  os.listdir('E:/机器学习实战/Ch02/testDigits')
    errorCount = 0.0
    mTest = len(testFileList) 
    for i in range(mTest):
        fileNameStr = testFileList[i]
        filestr = fileNameStr.split('.')[0]
        classNumStr = eval(filestr.split('_')[0])
        vectorUnderTest = img2vector('E:/机器学习实战/Ch02/testDigits/' + fileNameStr)
        #已经在0-1之间不需要归一化
        classifierResult = classify0(vectorUnderTest,trainingMat,Labels,3)
        #print("the classifier came back with:{},the real answer is:{}".format(classifierResult,classNumStr))
        if classNumStr != classifierResult :    errorCount += 1
    print("\nthe total number of error is :{}".format(errorCount))
    print("\nthe total error rate is :{}".format(errorCount/float(mTest)))

handwritingClassTest()





