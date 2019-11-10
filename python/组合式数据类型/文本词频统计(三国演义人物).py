import jieba
'''
#词频统计
txt = open("threekingdoms.txt","r",encoding="utf-8").read()
words = jieba.lcut(txt)
counts = {}
for word in words:
    if len(word) == 1:  #去掉标点，特殊符号
        continue
    else:
        counts[word] = counts.get(word,0) + 1
items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
for i in range(20):
    word,count = items[i]
    #print("{0:<10}{1:>5}".format(word,count))
'''

#人物出场统计 去除一些非人名
#txt = open("threekingdoms.txt","r",encoding="utf-8").read()
txt = open("TXT.txt","r",encoding="utf-8").read()
excludes = {"将军","却说","荆州","二人","不可","不能","如此"}
words = jieba.lcut(txt)
counts = {}
for word in words:
    if len(word) == 1:  #去掉标点，特殊符号
        continue
    elif word == "诸葛亮" or word == "孔明曰":
        rword = "孔明"
    elif word == "关公" or word == "云长":
        rword = "关羽"
    elif word == "玄德" or word == "玄德曰":
        rword = "刘备"
    elif word == "孟德" or word == "丞相":
        rword = "曹操"
    else:
        rword = word
    counts[rword] = counts.get(rword,0) + 1  #注意换行后的间隔
'''    
for i in excludes:
    del counts[i]
'''
items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
for i in range(10):
    word,count = items[i]
    print("{0:<10}{1:>5}".format(word,count))





























    
