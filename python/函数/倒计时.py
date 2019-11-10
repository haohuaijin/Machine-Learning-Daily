import turtle
def drawGap():
    turtle.penup()  #小间隔
    turtle.fd(5)
def drawLine(draw): #画线
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    drawGap()
    turtle.right(90)
def drawDight(dight):   #绘制数字
    drawLine(True) if dight in [2,3,4,5,6,8,9] else drawLine(False)
    drawLine(True) if dight in [0,1,3,4,5,6,7,8,9] else drawLine(False)
    drawLine(True) if dight in [0,2,3,5,6,8,9] else drawLine(False)
    drawLine(True) if dight in [0,2,6,8] else drawLine(False)
    turtle.left(90)
    drawLine(True) if dight in [0,6,80,4,5,6,8,9] else drawLine(False)
    drawLine(True) if dight in [0,2,3,5,6,7,8,9] else drawLine(False)
    drawLine(True) if dight in [0,1,2,3,4,7,8,9] else drawLine(False)
    turtle.penup()
    turtle.left(180)
    turtle.fd(40)
def main(dight_0):
    turtle.setup(400,300,200,200)
    turtle.penup()
    turtle.pencolor('red')
    turtle.fd(-60)
    turtle.pensize(5)
    #turtle.speed(0.13) #加速
    
    drawDight((0 if (dight_0/10)%10 < 1 else int(dight_0/10)%10))#画数字
    drawDight(dight_0%10)
    
    turtle.hideturtle()
    turtle.reset()
    #turtle.done()
dight = input("请输入倒计时的时间：")
data = range(eval(dight))
data = data[::-1]#转置
for i in data:
    main(i)
turtle.done()


