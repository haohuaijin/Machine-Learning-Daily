import matplotlib.pyplot as plt 

from pylab import mpl  #解决中文乱码
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

def treeInfo(i):
    listOfTrees = [{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}},\
                   {'no surfacing':{0:'no',1:{'flippers':{0:{'head':{0:'no',1:\
                    'yes'}},1:'no'}}}}]
    return listOfTrees[i]


# boxstyle是文本框类型 fc是边框粗细 sawtooth是锯齿形
decisionNode = dict(boxstyle="sawtooth",fc="0.8")
leafNode = dict(boxstyle="round4",fc="0.8")
#引导线样式
arrow_args = dict(arrowstyle="<-")

#节点绘制(画布，文本，箭头终点，箭头起点，边框样式)
def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.axl.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',xytext=centerPt,\
                            textcoords='axes fraction',va='center',ha='center',bbox=nodeType,\
                            arrowprops=arrow_args)

def createPlot(inTree):   #画树
    fig = plt.figure(1,facecolor='white') #创建了一个新图形
    fig.clf() # 将画图清空
    axprops = dict(xticks=[],yticks=[])
    createPlot.axl = plt.subplot(111,frameon=False,**axprops)  # 设置一个多图展示，但是设置多图只有一个
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0 
    plotTree(inTree,(0.5,1.0),'')
    plt.show()

def getNumLeafs(Tree): #获取节点数
    numLeafs = 0
    firstStr = list(Tree.keys())[0] #tree.keys()类型不是list，先进行类型转化
    secondDict = Tree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs += 1
    return numLeafs

def getTreeDepth(Tree): #获取决策树的深度
    maxDepth = 0
    firstStr = list(Tree.keys())[0]
    secondDict = Tree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   thisDepth = 1
    if thisDepth > maxDepth:    maxDepth = thisDepth
    return maxDepth

def plotMidText(cntrPt,parentPt,txtString): #在父子节点间填充文本信息
    xMid = ( parentPt[0] + cntrPt[0] ) / 2.0   #计算父子节点的中间位置
    yMid = ( parentPt[1] + cntrPt[1] ) / 2.0
    createPlot.axl.text(xMid,yMid,txtString)

def plotTree(Tree,parentPt,nodeTxt):
    numLeafs = getNumLeafs(Tree)
    depth = getTreeDepth(Tree)
    firstStr = list(Tree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt,parentPt,nodeTxt) #标记子节点的属性值
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict = Tree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD  #减少y的偏移
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leafNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD


''''
tree = treeInfo(0)
#tree['no surfacing'][3] = 'maybe'
createPlot(tree)
'''

















