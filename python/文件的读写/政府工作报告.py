#绘制词云
import jieba
import wordcloud
#from scipy.misc import imresd     
from imageio import imread
mask = imread("chinamap.jpg")    #导入五角星图片
#f = open("新时代中国特色社会主义.txt","r",encoding="utf-8")
f = open("新时代中国特色社会主义.txt","r",encoding="utf-8")
t = f.read()
f.close()
ls = jieba.lcut(t)  #返回列表
txt = " ".join(ls)  # 用空格分开
w = wordcloud.WordCloud( font_path = "msyh.ttc",mask = mask,\
                         width = 1000,height = 700,background_color = "white",\
                         )#max_words = 15
w.generate(txt)
w.to_file("grwordcloud.png")
