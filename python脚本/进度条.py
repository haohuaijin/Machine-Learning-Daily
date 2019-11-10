#text.py
'''
import time
scale = 10
print("{0:-^20}".format("执行开始"))
for i in range(scale + 1):
    a = '*' * i
    b = '.' * (scale - i)
    c = (i/scale)*100
    print("{:^3.0f}%[{}->{}]".format(c,a,b))
    time.sleep(0.1)
print("{0:-^20}".format("执行结束"))
'''

import time
for i in range(101):
    print("\r{:3}%".format(i),end="")
    time.sleep(0.06)

