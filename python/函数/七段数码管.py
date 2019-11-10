import turtle
import time
def drawGap():           #怎加小间隔
    turtle.penup()
    turtle.fd(5)
def drawLine(draw):      #绘制单段数码管
    drawGap()
    turtle.pendown() if draw else turtle.penup()
    turtle.fd(40)
    drawGap()
    turtle.right(90)
def drawDight(dight):    #根据数字绘制七段数码管
    drawLine(True) if dight in [2,3,4,5,6,8,9] else drawLine(False)
    drawLine(True) if dight in [0,1,3,4,5,6,7,8,9] else drawLine(False)
    drawLine(True) if dight in [0,2,3,5,6,8,9] else drawLine(False)
    drawLine(True) if dight in [0,2,6,8] else drawLine(False)
    turtle.left(90)
    drawLine(True) if dight in [0,6,80,4,5,6,8,9] else drawLine(False)
    drawLine(True) if dight in [0,2,3,5,6,7,8,9] else drawLine(False)
    drawLine(True) if dight in [0,1,2,3,4,7,8,9] else drawLine(False)
    turtle.left(180)
    turtle.penup()      #为后续的绘制做准备
    turtle.fd(20)   
def drawData(data):     #获得要输出的数字 data格式为'%Y-%m=%d+'
    turtle.pencolor("red")
    for i in data:     
      if i == '-' :
          turtle.write("年",font=("Arial",18,"normal"))
          turtle.pencolor("green")
          turtle.fd(40)
      elif i == '=':
          turtle.write("月",font=("Arial",18,"normal"))
      elif i == '+':
          turtle.write("日",font=("Arial",18,"normal"))
      else:
          drawDight(eval(i))
def main():
    turtle.setup(800,350,200,200)
    turtle.penup()
    turtle.fd(-300)
    turtle.pensize(5)
    drawData(time.strftime("%Y-%m=%d+",time.gmtime()))
    turtle.hideturtle()
    turtle.reset()
    turtle.done()

main() #运行











































