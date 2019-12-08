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

class optStruct: 
    def __init__(self,dataMatIn,classLabels,C,toler):
        self.X = dataMatIn
        self.labelMat = classLabels
        self.C = C
        self.tol = toler
        self.m = shape(dataMatIn)[0]
        self.alphas = mat(zeros((self.m,1)))
        self.b = 0
        self.eCache = mat(zeros((self.m,2)))

def calcEk(oS,k): #计算误差,并返回
    fXk = float(multiply(oS.alphas,oS.labelMat).T*\
                (oS.X*oS.X[k,:].T)) + oS.b  #为什么他可以(oS.X*oS.X[k,:].T)(画图)
    Ek = fXk - float(oS.labelMat[k])
    return Ek

def selectJ(i,oS,Ei):  #选择内循环的alpha
    maxK = -1
    maxDeltaE = 0
    Ej = 0
    oS.eCache[i] = [1,Ei]
    valiEcacheList = nonzero(oS.eCache[:,0].A)[0]  #构建一个非零列表
    if(len(valiEcacheList)) > 1:
        for k in valiEcacheList:
            if k == i: continue
            Ek = calcEk(oS,k)
            deltaE = abs(Ei - Ek)
            if (deltaE > maxDeltaE):
                maxK = k
                maxDeltaE = deltaE
                Ej = Ek
        return maxK,Ej
    else:
        j = selectJrand(i,oS.m)
        Ej = calcEk(oS,j)
    return j,Ej

def updateEk(oS,k): #储存误差
    Ek = calcEk(oS,k)
    oS.eCache[k] = [1,Ek]


def innerL(i,oS):
    Ei = calcEk(oS,i)
    if((oS.labelMat[i]*Ei < -oS.tol) and (oS.alphas[i] < oS.C)) or\
        ((oS.labelMat[i]*Ei > oS.tol) and (oS.alphas[i] > 0)):
        j,Ej = selectJ(i,oS,Ei)
        alphaIold = oS.alphas[i].copy()
        alphaJold = oS.alphas[j].copy()
        if(oS.labelMat[i] != oS.labelMat[j]):
            L = max(0,oS.alphas[j] - oS.alphas[i])
            H = min(oS.C,oS.C + oS.alphas[j] - oS.alphas[i])
        else:
            L = max(0,oS.alphas[i] + oS.alphas[i] - oS.C)
            H = min(oS.C,oS.alphas[j] + oS.alphas[i])
        if L == H: print("L==H"); return 0
        eta = 2.0*oS.X[i,:]*oS.X[j,:].T - oS.X[i,:]*oS.X[i,:].T - \
            oS.X[j,:]*oS.X[j,:].T
        if eta >= 0: print("eta>=0"); return 0
        oS.alphas[j] -= oS.labelMat[j]*(Ei-Ej)/eta
        oS.alphas[j] = clipAlpha(oS.alphas[j],H,L)
        updateEk(oS,j)
        if(abs(oS.alphas[j] - alphaJold) < 0.00001):
            print("j not moving enough")
            return 0
        oS.alphas[i] += oS.labelMat[j]*oS.labelMat[i]*\
                        (alphaJold - oS.alphas[j])
        updateEk(oS,i)
        b1 = oS.b - Ei - oS.labelMat[i]*(oS.alphas[i] - alphaIold)*\
            oS.X[i,:]*oS.X[i,:].T - oS.labelMat[j]*\
            (oS.alphas[j] - alphaJold)*oS.X[i,:]*oS.X[j,:].T
        b2 = oS.b - Ej - oS.labelMat[i]*(oS.alphas[i] - alphaIold)*\
            oS.X[i,:]*oS.X[j,:].T - oS.labelMat[j]*\
            (oS.alphas[j] - alphaJold)*oS.X[j,:]*oS.X[j,:].T
        if(0 < oS.alphas[i]) and (oS.C > oS.alphas[i]): oS.b = b1
        elif(0 < oS.alphas[j]) and (oS.C > oS.alphas[j]): oS.b = b2
        else: oS.b = (b1 + b2)/2.0
        return 1
    else: return 0

def smoP(dataMatIn,classLabels,C,toler,maxIter,kTup=('lin',0)):
    oS = optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler)
    iters = 0
    entireSet = True
    alphaPairsChanged = 0
    while(iters < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
        alphaPairsChanged = 0
        if entireSet:
            for i in range(oS.m):
                alphaPairsChanged += innerL(i,oS)
            print("fullSet,iters: %d i: %d,pairs changed %d"%(iters,i,alphaPairsChanged))
            iters += 1
        else:
            nonBoundIs = nonzero((oS.alphas.A > 0)*(oS.alphas.A < C))[0]
            for i in nonBoundIs:
                alphaPairsChanged += innerL(i,oS)
                print("non-bound,iter: %d i%d,pairs changed %d"%(iters,i,alphaPairsChanged))
            iters += 1
        if entireSet: entireSet = False
        elif(alphaPairsChanged == 0): entireSet = True
        print("iteration number: %d"%iters)
    return oS.b,oS.alphas

def calcWs(alphas,dataArr,classLabels):
    X = mat(dataArr)
    labelMat = mat(classLabels).transpose()
    m,n = shape(X)
    w = zeros((n,1))
    for i in range(m):
        w += multiply(alphas[i]*labelMat[i],X[i,:].T)
    return w


data,label = loadDataSet('testSet.txt')
b,alphas = smoP(data,label,0.6,0.001,40)
ws = calcWs(alphas,data,label)



a = array(data)
plt.figure()
n = array(label) 
plt.scatter(a[n==1,0],a[n==1,1],color='r')
plt.scatter(a[n==-1,0],a[n==-1,1],color='b')
plt.show()
















    
