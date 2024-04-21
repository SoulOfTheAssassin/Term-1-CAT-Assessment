from inputimeout import inputimeout 
import time
import sys
times = 10
try: 
    time_over = inputimeout(prompt='Name your best friend:', timeout=times) 
    for char in time_over:
        print(char, end='')
        sys.stdout.flush()
        time.sleep(0.03)
    time.sleep(1)

except Exception: 
    time_over = 'Your time is over!'
    print(time_over) 