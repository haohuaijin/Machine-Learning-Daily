def Getnum():   #获取用户不定长度的输入
    nums = []
    inumstr = input("请输入数字(回车退出):")
    while inumstr != "":
        nums.append(eval(inumstr))
        inumstr = input("请输入数字(回车退出):")
    return nums #注意return的位置

def Mean(nums):  #计算平均值
    s = 0.0
    for i in nums:
        s = s + i
    return s/len(nums)

def dev(nums,mean):  #计算方差
    sdev = 0.0
    for i in nums:
        sdev = sdev + (i-mean)**2
    return pow(sdev / (len(nums)-1),0.5)

def median(nums):   #计算中位数
    sorted(nums)    #排序函数
    size = len(nums)
    if size % 2 == 0:
        med = (nums[size//2-1] + nums[size//2])/2
    else:
        med = nums[size//2]
    return med

n = Getnum()
m = Mean(n)
print("平均值:{},方差:{:.2},中位数:{}".format(m,dev(n,m),median(n)))
