from timer_cm import *
import os, sys, time

def demo_performance_timer():

    with Timer('main timer') as tm:
        with tm.child('short subtask'):
            print("I'm super quick !")
        with tm.child('medium subtask'):
            time.sleep(0.5)
            print('Half a second, give or take')
        with tm.child('long subtask'):
            for i in range(10000):
                for j in range(5000):
                    x = (i*j)
            print('Phew all done!')


if __name__ == '__main__':
    demo_performance_timer()




