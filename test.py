import threading
from time import sleep

def func1():
    while True:
        sleep(1)
        print("A")
def func2():
    while True:
        sleep(2)
        print("B")

f1 = threading.Thread(target=func1)
f2 = threading.Thread(target=func2)

f1.start()
f2.start()


# event handler thread
# main loop thread