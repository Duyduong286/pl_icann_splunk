from schedule import every, repeat, run_pending
import time

global x 
x = 10

@repeat(every(3).seconds)
def yee():
    global x
    x = x + 3
    print(x)

while x != 80:
    run_pending()
    time.sleep(1)