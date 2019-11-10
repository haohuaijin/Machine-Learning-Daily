def rvs(s):    #反转字符串
    if s == "":
        return s
    else:
        return rvs(s[1:]) + s[0]


def f(n):   #斐波那契数列
    if n==1 or n==2:
        return 1
    else:
        return f(n-1) + f(n-2)

count = 0
def hanoi(n,src,dst,mid):
    global count
    if n == 1:
        print("{}:{}->{}".format(1,src,dst))  #层数逐渐减少，最后只剩第一层
        count += 1
    else:
        hanoi(n-1,src,mid,dst)
        print("{}:{}->{}".format(n,src,dst))
        count += 1
        hanoi(n-1,mid,dst,src)

print(rvs("hello"))
print(f(9))
hanoi(3,"A","C","B")
print(count)
