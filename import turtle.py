import turtle

# Sample data
data = [1853, 1992, 21.2, 21.7, 22.8, 22.2, 22.0, 20.8, 25.1, 19.3, 19.7, 19.9, 21.8, 22.8, 22.3, 21.7, 20.3, 25.8, 24.1, 24.9, 21.1, 23.7, 22.6, 25.3, 19.9, 24.5, 21.1, 22.2, 17.5, 19.7, 22.7, 20.0]

# Sorting the data
data.sort()

# Calculating the quartiles
q1 = data[int(len(data) * 0.25)]
q2 = data[int(len(data) * 0.5)]
q3 = data[int(len(data) * 0.75)]

# Calculating the interquartile range
iqr = q3 - q1

# Calculating the lower and upper bounds
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Creating a turtle window
turtle.setup(800, 600)
window = turtle.Screen()
window.bgcolor("white")

# Creating a turtle for the box plot
t = turtle.Turtle()
t.speed(0)
t.penup()
t.goto(-200, 0)
t.pendown()
t.pensize(2)

# Drawing the box plot
t.fillcolor("gray")
t.begin_fill()
t.forward(400)
t.left(90)
t.forward((q1 - lower_bound) * 20)
t.right(90)
t.forward((q3 - q1) * 20)
t.right(90)
t.forward((q2 - q1) * 20)
t.right(90)
t.forward((q3 - q2) * 20)
t.right(90)
t.forward((upper_bound - q3) * 20)
t.right(90)
t.forward((q3 - q1) * 20)
t.right(90)
t.forward((upper_bound - q3) * 20)
t.left(90)
t.forward(400)
t.end_fill()

# Creating a turtle for the histogram
t2 = turtle.Turtle()
t2.speed(0)
t2.penup()
t2.goto(-200, -200)
t2.pendown()
t2.pensize(2)