import matplotlib.pyplot as plt 
import math
import time

pi = 3.14159

fig, ax = plt.subplots()

x = []
y = []

def PointsInCircum(r,n=20):
    circle = [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]
    return circle

circle_list = PointsInCircum(3, 50)

for t in range(len(circle_list)):
    if t == 0:
        points, = ax.plot(x, y, marker='o', linestyle='--')
        ax.set_xlim(-4, 4) 
        ax.set_ylim(-4, 4) 
        plt.show()
    else:
        x_coord, y_coord = circle_list.pop()
        x.append(x_coord)
        y.append(y_coord)
        points.set_data(x, y)
    plt.pause(0.1)
#    plt.draw()
    time.sleep(0.1)