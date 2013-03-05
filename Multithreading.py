#!/usr/bin/env python

import threading, random
from time import ctime, sleep

'''
1. Populate the source array
2. Define the formula method. 
3. For each new thread, have it named.
4. For each thread, 
4.1. have it acquire the lock, read the value and release the lock;
4.2. have it perform the necessary factorial computation (use recursion).
4.3. have it acquire the second lock to write to a second array storing all the computed values
and then release the lock.
4.4. have the thread print that it is completed and its name/number.
4.5. Repeat the process again until number of items in the 

'''

# Global variables
# MAX_THREAD_NUM = 5
SOURCE_INPUT_POS = 0
sourceInput = [x for x in range(10)]
sourceOutput = []

###################################################################################################
# Lock 0 and 1 are for reading and writing to sourceInput and sourceOutput arrays respectively,   #
# Lock 2 is for creating new threads when the number of threads is not at MAX_THREAD_NUM          #
#                                                                                                 #

locks = []
locks.append(threading.RLock()) # Lock 0 for reading 
locks.append(threading.RLock()) # Lock 1 for writing
                                                                                                 
###################################################################################################


class MyThread(threading.Thread):
    def __init__(self,num):
        threading.Thread.__init__(self)
        self.num = num
        self.name = "Thread-%d", self.num
        
    def run(self):
        global locks
        global SOURCE_INPUT_POS
        
        # Acquire lock for reading sourceInput array, read from array, increase reading pointer by 1, release lock
        locks[0].acquire()        
        element = sourceInput[SOURCE_INPUT_POS]
        SOURCE_INPUT_POS += 1        
        locks[0].release()

        print 'Have read %d from the sourceInput list.', element

        factorialValue = self.factorial()
        
        #Acquire lock for writing to sourceOutput array, write to array, release lock.
        locks[1].acquire()
        sourceOutput.append(factorialValue)
        locks[1].release()
        
        print self.name, " is completed." # thread is completed.
        
    def factorial(self):
        product = 1
        for i in range(1, self.num+1): #range is from 1 and includes limit
            product *= i
        
        return product
 
    
print 'Starting the main thread at: ', ctime()

while(SOURCE_INPUT_POS < len(sourceInput)):
    MyThread(sourceInput[SOURCE_INPUT_POS]).start()
    
    sleep(random.random()* 5)

print 'The computed output: \n', sourceOutput
print 'Main thread completed at: ', ctime()        # This is going to print before threads complete.
