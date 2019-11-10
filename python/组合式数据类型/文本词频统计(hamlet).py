def getText():    #文本预处理
    txt = open("hamlet.txt","r",encoding="UTF-8").read()
    txt = txt.lower()
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
        txt = txt.replace(ch," ")
    return txt

hamletTxt = getText()
words = hamletTxt.split()

counts = {}   #字典类型
for word in words:    #统计
    counts[word] = counts.get(word,0) + 1
    
items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)  #排序 lambda 是定义一个函数

for i in range(10):
    word,count = items[i]
    print("{0:<10}{1:>5}".format(word,count))
