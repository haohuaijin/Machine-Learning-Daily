from numpy import *  #引用全部的numpy,对numpy中的函数可以直接使用
import operator
import matplotlib.pyplot as plt

def createDataSet():   #创造数据
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels

def classify0(inX,dataSet,labels,k):  #对向量进行分类
	dataSetSize = dataSet.shape[0]               #行数
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








































