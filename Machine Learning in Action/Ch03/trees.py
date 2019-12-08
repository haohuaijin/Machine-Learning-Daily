from math import log
import operator

def treeInfo(i):   #已经建立好的树
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},\
                   {'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:\
                    'yes'}},1:'no'}}}}]
    return listOfTrees[i]

def majroityCnt(classList):   #投票选出叶子节点的类别
    classCount = {}
    for vote in classList:
        #if vote not in classCount.keys():  classCount[vote] = 0
        #classCount[vote] += 1
        classCount[vote] = classCount.get(vote,0) + 1
    sortData = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortData[0][0]

def creatDataSet():
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing','flippers']
    return dataSet,labels

def calcShannonEnt(dataSet):   #计算香农熵
    numEntries = len(dataSet)
    labelsCount = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelsCount.keys():
            labelsCount[currentLabel] = 0
        labelsCount[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelsCount:             #计算香农熵
        prob = float(labelsCount[key])/numEntries
        shannonEnt -= prob*log(prob,2)
    return shannonEnt

#dataSet:数据集 axis:划分数据集的特征 value:需要返回的特征的值
def splitDataSet(dataSet,axis,value):   #按指定的特征划分数据集
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet  #按照某个特征划分数据集,需要将服药要求的元素抽取出来

'''
1、对每一个特征形成列表
2、遍历当前特征的所有唯一属性
3、对每一个属性划分一次数据集(对dataSet)，计算信息熵
4、计算信息增益(信息增益是熵的减少或者是数据无序度的减少)
'''
def chooseBestFeatureToSplit(dataSet):  #选择最好的数据集划分方式(特征)
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]  #创建第i个特征的分类标签
        uniqueVals = set(featList) #转化为集合(去掉重复的元素)
        newEntropy = 0.0
        for value in uniqueVals:    #计算每种划分方式的信息熵
            subDataSet = splitDataSet(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy-newEntropy  #计算信息增益
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
        #print(infoGain) 打印信息增益
    return bestFeature

def createTree(dataSet,labels):     #创造决策树
    classList = [example[-1] for example in dataSet]  #?
    if classList.count(classList[0]) == len(classList):  #属于同一类别返回
        return classList[0] 
    if len(dataSet[0]) == 1:        #没有可以划分的特征返回
        return majroityCnt(ClassList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    Tree = {bestFeatLabel:{}}       #嵌套字典，得到当前的最好标签
    del(labels[bestFeat])           #删除已经用了的特征
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)    #得到当前选择特征的所有属性值
    for value in uniqueVals:
        subLabels = labels[:]
        #下面使用嵌套字典来递归建立决策树
        Tree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,\
                                                            value),subLabels)
    return Tree

def classify(Tree,featLabels,testVec):  #使用决策树
    firstStr = list(Tree.keys())[0]
    secondDict = Tree[firstStr]
    featIndex = featLabels.index(firstStr) #找到第一个分类的属性
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__=='dict':
                classLabel = classify(secondDict[key],featLabels,testVec)
            else:   classLabel = secondDict[key]
    return classLabel

'''
使用pickle模块在磁盘上保存决策树
'''
def storeTree(Tree,filename):
    import pickle
    fw = open(filename,'wb+')
    pickle.dump(Tree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename,'rb')
    return pickle.load(fr)


import treePlotter as tp 

def main():
    fr = open('lenses.txt')
    lenses = [line.strip().split('\t') for line in fr.readlines()]
    lensesLabels = ['age','prescript','astigmatic','tearRate']
    lensesTree = createTree(lenses,lensesLabels.copy())
    print(lensesTree)
    tp.createPlot(lensesTree)


main()


'''
Data,labels = creatDataSet()
print(Data,labels)
tree = createTree(Data,labels.copy()) #.copy()是引用值，不是指针，不改变原来的数据
print(Data,labels)
#tree = treeInfo(0)
result = classify(tree,labels,[1,0])
print(result)
#print(tree)
'''

'''
feature = chooseBestFeatureToSplit(Data)
print(feature)
a = calcShannonEnt(Data)
print(splitDataSet(Data,0,1))
print(splitDataSet(Data,0,0))
'''
