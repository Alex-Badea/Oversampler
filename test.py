import multiprocessing
import numpy as np
from math import sqrt, sin
import time

def expenser_tester(num):
   return sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(sin(num))))))))))))))))))))))

if __name__ == '__main__':
    n = 3000
    starttime1 = time.time()
    pool = multiprocessing.Pool(2)
    pool_outputs = pool.map(expenser_tester, range(n))
    pool.close()
    pool.join()
    endtime1 = time.time()
    timetaken = endtime1 - starttime1

    starttime2 = time.time()
    for i in range(n):
        expenser_tester(i)
    endtime2 = time.time()
    timetaken2 = endtime2 - starttime2

    print('The time taken with multiple processes:', timetaken)
    print('The time taken the usual way:', timetaken2)
