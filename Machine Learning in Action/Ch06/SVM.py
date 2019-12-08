from numpy import*
import matplotlib.pyplot as plt

def loadDataSet(fileName): 
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = line.strip().split('\t')
        dataMat.append([float(lineArr[0]),float(lineArr[1])])
        labelMat.append(float(lineArr[2]))
    return dataMat,labelMat

def selectJrand(i,m): #只要函数值不等于输入值i，函数就会进行随机选择
    j = i
    while(j == i):
        j = int(random.uniform(0,m))
    return j 

def clipAlpha(aj,H,L): #用于调整大于H或小于L的alpha值
    if aj > H:
        aj = H
    if L > aj:
        aj = L 
    return aj

#简化SMO算法
def smoSimple(dataMatIn,classLabels,C,toler,maxIter):
    '''
    @dataMat    ：数据列表
    @classLabels：标签列表
    @C          ：权衡因子（增加松弛因子而在目标优化函数中引入了惩罚项）
    @toler      ：容错率
    @maxIter    ：最大迭代次数
    '''
    dataMatrix = mat(dataMatIn)
    labelMat = mat(classLabels).transpose()  #转置后是列向量
    b = 0
    m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iters = 0
    while(iters < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            #预测的结果
            fXi = float(multiply(alphas,labelMat).T*\
                        (dataMatrix*dataMatrix[i,:].T)) + b
            #预测值与真实值的误差
            Ei = fXi - float(labelMat[i])
            #如果误差比较大,对alpha进行优化
            if(((labelMat[i]*Ei < -toler) and (alphas[i] < C)) or \
                ((labelMat[i]*Ei > toler) and (alphas[i] > 0))):
                #随机选择第二个alpha，进行优化
                j = selectJrand(i,m)
                fXj = float(multiply(alphas,labelMat).T*\
                            (dataMatrix*dataMatrix[j,:].T)) + b
                Ej = fXj - float(labelMat[j])
                #复制alpha[i]和alpha[j]的值，用于后续的比较
                #通过.copy()只复制值，不引用地址
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if(labelMat[i] != labelMat[j]):
                    L = max(0,alphas[j] - alphas[i])
                    H = min(C,C + alphas[j] - alphas[i])
                else:
                    L = max(0,alphas[j] + alphas[i] - C)
                    H = min(C,alphas[j] + alphas[i])
                #如果L == H 则不做任何改变,countinue
                if L == H:
                    print("L==H")
                    continue
                #alpha[j]的最优修改量
                eta = 2.0*dataMatrix[i,:]*dataMatrix[j,:].T - \
                    dataMatrix[i,:]*dataMatrix[i,:].T - \
                    dataMatrix[j,:]*dataMatrix[j,:].T
                #如果eta = 0,由于下面要除以eta,所以退出循环
                if eta >= 0: print("eta>=0"); continue
                alphas[j] -= (labelMat[j]*(Ei - Ej))/eta
                #用clipAlpha来调整alpha[j]的值在L < alpha[j] < H
                alphas[j] = clipAlpha(alphas[j],H,L)
                #若alpha[j]只有轻微的变化，退出循环
                if(abs(alphas[j] - alphaJold) < 0.00001):
                    print("j not moving enough")
                    continue
                #alpha[i]和alpha[j]同样进行改变
                #给alpha[i]和alpha[j]设置常数项                
                alphas[i] += labelMat[j]*labelMat[i]*\
                            (alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i] - alphaIold)*\
                    dataMatrix[i,:]*dataMatrix[i,:].T - \
                    labelMat[j]*(alphas[j] - alphaJold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ej - labelMat[i]*(alphas[i] - alphaIold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T - \
                    labelMat[j]*(alphas[j] - alphaJold)*\
                    dataMatrix[j,:]*dataMatrix[j,:].T
                if (0 < alphas[i]) and (C > alphas[i]): b = b1
                elif (0 < alphas[j]) and (C > alphas[j]): b = b2
                else: b = (b1 + b2)/2.0
                #记录alpha改变的对数
                alphaPairsChanged += 1
                print("iter: %d i: %d,pairs changed %d"%(iters,i,alphaPairsChanged))
        #只有遍历数据值maxIter次，并且不再发生alpha修改后，退出程序
        if(alphaPairsChanged == 0): iters += 1
        else: iters = 0
        print("iteration number: %d"%iters)
    return b,alphas



'''
def smoSimple(dataMat,classLabels,C,toler,maxIter):
    
    @dataMat    ：数据列表
    @classLabels：标签列表
    @C          ：权衡因子（增加松弛因子而在目标优化函数中引入了惩罚项）
    @toler      ：容错率
    @maxIter    ：最大迭代次数
    
    #将列表形式转为矩阵或向量形式
    dataMatrix=mat(dataMat);labelMat=mat(classLabels).transpose()
    #初始化b=0，获取矩阵行列
    b=0;m,n=shape(dataMatrix)
    #新建一个m行1列的向量
    alphas=mat(zeros((m,1)))
    #迭代次数为0
    iters=0
    while(iters<maxIter):
        #改变的alpha对数
        alphaPairsChanged=0
        #遍历样本集中样本
        for i in range(m):
            #计算支持向量机算法的预测值
            fXi=float(multiply(alphas,labelMat).T*\
            (dataMatrix*dataMatrix[i,:].T))+b
            #计算预测值与实际值的误差
            Ei=fXi-float(labelMat[i])
            #如果不满足KKT条件，即labelMat[i]*fXi<1(labelMat[i]*fXi-1<-toler)
            #and alpha<C 或者labelMat[i]*fXi>1(labelMat[i]*fXi-1>toler)and alpha>0
            if(((labelMat[i]*Ei < -toler)and(alphas[i] < C)) or \
            ((labelMat[i]*Ei>toler) and (alphas[i]>0))):
                #随机选择第二个变量alphaj
                j = selectJrand(i,m)
                #计算第二个变量对应数据的预测值
 
                fXj = float(multiply(alphas,labelMat).T*(dataMatrix*\
                            dataMatrix[j,:].T)) + b
                #计算与测试与实际值的差值
                Ej = fXj - float(labelMat[j])
                #记录alphai和alphaj的原始值，便于后续的比较
                alphaIold=alphas[i].copy()
                alphaJold=alphas[j].copy()
                #如何两个alpha对应样本的标签不相同
                if(labelMat[i]!=labelMat[j]):
                    #求出相应的上下边界
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C,C+alphas[j]-alphas[i])
                else:
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                if L==H: print("L==H");continue
                #根据公式计算未经剪辑的alphaj
                #------------------------------------------
                eta=2.0*dataMatrix[i,:]*dataMatrix[j,:].T-\
                    dataMatrix[i,:]*dataMatrix[i,:].T-\
                    dataMatrix[j,:]*dataMatrix[j,:].T
                #如果eta>=0,跳出本次循环
                if eta>=0:print("eta>=0"); continue
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                #------------------------------------------    
                #如果改变后的alphaj值变化不大，跳出本次循环    
                if(abs(alphas[j]-alphaJold)<0.00001):print("j not moving\
                enough");continue
                #否则，计算相应的alphai值
                alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j])
                #再分别计算两个alpha情况下对于的b值
                b1 = b - Ei- labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]\
                 *dataMatrix[i,:].T - labelMat[j]*(alphas[j]-alphaJold)*\
                 dataMatrix[i,:]*dataMatrix[j,:].T
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*\
                    dataMatrix[i,:]*dataMatrix[j,:].T-\
                    labelMat[j]*(alphas[j]-alphaJold)*\
                    dataMatrix[j,:]*dataMatrix[j,:].T
                #如果0<alphai<C,那么b=b1
                if(0<alphas[i]) and (C>alphas[i]):b=b1
                #否则如果0<alphai<C,那么b=b1
                elif (0<alphas[j]) and (C>alphas[j]):b=b2
                #否则，alphai，alphaj=0或C
                else:b=(b1+b2)/2.0
                #如果走到此步，表面改变了一对alpha值
                alphaPairsChanged+=1
                print("iters: %d i:%d,paird changed %d" %(iters,i,alphaPairsChanged))
        #最后判断是否有改变的alpha对，没有就进行下一次迭代
        if(alphaPairsChanged==0):iters+=1
        #否则，迭代次数置0，继续循环
        else:iters=0
        print("iteration number: %d" %iters)
    #返回最后的b值和alpha向量
    return b,alphas
'''


data,label = loadDataSet("testSet.txt")
#plt.scatter()
#plt.show()
b,alphas = smoSimple(data,label,0.6,0.001,40)
for i in range(100):
    if alphas[i] > 0:
        print(alphas[i],label[i])
#print(label[0:5])
#print(data[0:3])



























