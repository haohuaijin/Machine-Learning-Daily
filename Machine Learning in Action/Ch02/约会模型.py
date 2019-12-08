from numpy import *  #引用全部的numpy,对numpy中的函数可以直接使用
import operator
import matplotlib.pyplot as plt

def classify0(inX,dataSet,labels,k):  #对向量进行分类
	#dataSetSize = dataSet.shape[0]                #行数
	#diffMat = tile(inX,(dataSetSize,1))-dataSet  #对向量进行复制，得到和dataSet一样的大小
	diffMat = inX-dataSet                         #利用广播更加简单
	sqDiffMat = diffMat**2                        #各个维度的平方
	sqDistances = sqDiffMat.sum(axis=1)
	distances = sqDistances**0.5
	sortedDistIndicies = distances.argsort()
	classCount = {}
	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
	sortedClassCount = sorted(classCount.items(),key = operator.itemgetter(1),reverse = True)
	return sortedClassCount[0][0]

def file2matrix(filename):   #解析文本
	fr = open(filename)
	arrayOLines = fr.readlines()
	numberOfLines = len(arrayOLines)
	returnMat = zeros((numberOfLines,3))
	classLabelVector = []
	index = 0
	for line in arrayOLines:
	    line = line.strip()
	    listFormLine = line.split('\t')     #按照Tab键将列表分割
	    returnMat[index,:] = listFormLine[0:3]
	    classLabelVector.append(int(listFormLine[-1]))
	    index += 1
	return returnMat,classLabelVector

def autoNorm(dataSet):     #归一化，防止受单个数值大的特征的影响
    maxVals = dataSet.max(0)
    minVals = dataSet.min(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    normDataSet = dataSet - minVals   #利用广播
    normDataSet = normDataSet/ranges  #利用广播
    return normDataSet,ranges,minVals

'''
def datingClassTest():    #测试算法
    testRate = 0.10
    datingDataMat,datingLabels = file2matrix('E:\机器学习实战\Ch02\datingTestSet2.txt')
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]  #行数
    testData = int(m*testRate)
    errorCount = 0.0
    for i in range(testData):
        classifierResult = classify0(normMat[i,:],normMat[testData:m,:],\
                           datingLabels[testData:m],3)
        print("the classifier came back with:{},the real answer is:{}".format(\
            classifierResult,datingLabels[i]))
        if classifierResult != datingLabels[i]:   errorCount += 1
    print("the total error rate is:{}".format(errorCount/float(testData)))
'''

def classifyPerson():  #预测  #input()函数默认str型
    resultList = ['not at all','in small doses','in large doses']
    precentTats = eval(input("precentage of time spent playing video games?"))
    ffMiles = eval(input("frequent flier miles earned per years?"))
    iceCream = eval(input("Liters of ice Cream consumed per  year?"))
    datingDataMat,datingLabels = file2matrix('E:\机器学习实战\Ch02\datingTestSet2.txt')#解析文本
    normMat,ranges,minVals = autoNorm(datingDataMat)    #归一化
    Data = array([ffMiles,precentTats,iceCream])        #合并输入的数据
    classifierResult = classify0((Data-minVals)/ranges,normMat,datingLabels,3)
    print("You will probably like this perdon: {}".format(resultList[classifierResult-1]))

classifyPerson()

''' #画图
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,0],datingDataMat[:,1],\
           5.0*array(datingLabels),5.0*array(datingLabels))
plt.show()
'''












