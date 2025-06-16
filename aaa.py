# Game Development
# Turtle kutubxonasi!  ->  kodlar yordamida grafik hosil qilish uchun ishlatiladi!
import random
import time
import turtle

win = turtle.Screen()
win.title("Welcome To Our Gonka Club")
win.bgcolor('#484848')   #rgb(red, green, blue) | #rrggbb   | 0-f(16 lik sanoq sistemasi )

# poyga boshlandi! FORSAJ no way to turtle

finish = turtle.Turtle()
finish.penup()
finish.speed(0)
finish.color("white")
# startni chizish
finish.goto(300, 225)
finish.pendown()
finish.pensize(5)
finish.goto(300, -225)
finish.penup()

finish.hideturtle()
finish.pensize(2)

finish.goto(-310, 150)
finish.pendown()
finish.goto(300, 150)
finish.penup()
finish.goto(-310, 110)
finish.pendown()
finish.goto(300, 110)
finish.penup()
finish.goto(-310, 40)
finish.pendown()
finish.goto(300, 40)
finish.penup()
finish.goto(-310, 0)
finish.pendown()
finish.goto(300, 0)
finish.penup()
finish.goto(-310, -70)
finish.pendown()
finish.goto(300, -70)
finish.penup()
finish.goto(-310, -110)
finish.pendown()
finish.goto(300, -110)
finish.penup()
finish.goto(0, 225)


# poygachilar!!  red green black

red = turtle.Turtle()
red.color("red")
red.shape("turtle")
red.penup()
red.speed(0)
red.goto(-305, 130)


gr = turtle.Turtle()
gr.color("green")
gr.shape("turtle")
gr.penup()
gr.speed(0)
gr.goto(-305, 20)


black = turtle.Turtle()
black.color("black")
black.shape("turtle")
black.penup()
black.speed(0)
black.goto(-305, -90)

ranglar = {
    1: "green",
    2: "yellow",
    3: "red",
}

finish = turtle.Turtle()
finish.penup()
finish.speed(0)
finish.hideturtle()
finish.goto(0, 225)


for i in range(3, 0, -1):
    finish.clear()
    finish.color(ranglar[i])
    finish.write(f"{i}", align="center", font=("Arial", 24, "normal"))
    time.sleep(2)

finish.write("GO!!", align="center", font=("Arial", 24, "normal"))

finish.goto(0, 3)


while True:
    speed_bl = random.randint(1, 4)
    speed_red = random.randint(1, 4)
    speed_gr = random.randint(1, 4)
    black.forward(speed_bl)
    red.forward(speed_red)
    gr.forward(speed_gr)

    if red.xcor() >= 300:
        finish.clear()
        finish.color('red')
        finish.write("RED WINS!", align="center", font=("Arial", 24, "normal"))
        break

    if black.xcor() >= 300:
        finish.clear()
        finish.color('black')
        finish.write("BLACK WINS!", align="center", font=("Arial", 24, "normal"))
        break

    if gr.xcor() >= 300:
        finish.clear()
        finish.color('green')
        finish.write("GREEN WINS!", align="center", font=("Arial", 24, "normal"))
        break













win.mainloop()






















