import time
import sys

def slowinput(str, speed):
    for char in str:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(speed)
    c = input()
    return c

slowinput("Please enter a number: ", 0.08)
    