import threading
from time import sleep
from perlin_noise import PerlinNoise
import random
import opensimplex

def rand_grid():
    for i, row in enumerate(grid):
        for j,n in row:
            noise = opensimplex.noise2(x=i/COLS,y=j/ROWS)
            if noise > 0:
                n.colour = BARRIER_COLOUR

grid = []
ROWS, COLS = 100,100
def rand_grid():
    noise = PerlinNoise()
    for i,row in enumerate(grid):
        for j,n in row:
            if noise(i/ROWS,j/COLS) > 0 and (n.colour == BLANK_COLOUR or n.colour == PATH_COLOUR):
                n.colour = BARRIER_COLOUR



noise = PerlinNoise()
print(noise(random.randint(1,100)/100))

# def func1():
#     while True:
#         sleep(.5)
#         print("every .5 seconds")
# def func2():
#     while True:
#         sleep(1)
#         print("every 1 seconds")

# f1 = threading.Thread(target=func1)
# f2 = threading.Thread(target=func2)

# f1.start()
# f2.start()

# event handler thread
# main loop thread