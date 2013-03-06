#!/usr/bin/env python
 
import threading, random        # threading module has the Thread class from which we will inherit
                                # random module has the random method we will use to create random sleep times for threads.
 
from time import ctime, sleep   # ctime to record time for computation of threads
                                # sleep to put the threads to sleep at random times to slow down the threads.
 
# Global variables
SOURCE_INPUT_POS = 0                  # Keeps track of the next item to be read from the source list.
sourceInput = [x for x in range(10)]  # Source list for data that will have factorials computed against.
sourceOutput = []                     # List (empty for now) with computed factorials.
 
#############################################################################################################
# Locks will be used to lock reading and writing from the sourceInput and sourceOutput lists respectively.  #
# The locks will help to reduce possible deadlock and synchronisation issues caused by threads accessing    #
# the same list.                                                                                            #
 
locks = []
locks.append(threading.RLock()) # Lock 0 for reading from sourceInput List
locks.append(threading.RLock()) # Lock 1 for writing to sourceOutput List
                                                                                                 
#############################################################################################################

class MyThread(threading.Thread):               # Create a new class that inherits from the Thread class in the threading module
    def __init__(self,num):                     # Override the inherited __init__ method. Method takes a number used in naming.
        threading.Thread.__init__(self)         # Initialise the parent __init__ method.
        self.num = num                          
        self.name = "Thread-", self.num
        
    def run(self):
        global locks                            # The keyword global is used to give access to the locks and SOUCE_INPUT_POS variable
        global SOURCE_INPUT_POS                 # declared at the global level. 
        
        # Acquire lock for reading sourceInput list. Then read from array, increase reading pointer (SOUCE_INPUT_POS) by 1 to point 
        # to the next element to be read by the next thread and finally release lock for the next thread.
        locks[0].acquire()        
        element = sourceInput[SOURCE_INPUT_POS]
        SOURCE_INPUT_POS += 1        
        locks[0].release()
 
        print 'Have read ', element, ' from the sourceInput list.'    # To help us know where we are....
 
        factorialValue = self.factorial(element)   # Perform the factorial operation on the element and return the result.
        
        # Acquire lock for writing to sourceOutput list. Then append the factorial result to the list and then release the lock.
        # As we are appending to the list, there is no need to keep track of the next write position into the array.
        locks[1].acquire()
        sourceOutput.append(factorialValue)
        locks[1].release()
        
        print self.name, " is completed." # Notification that the thread has completed its operations.
        
    def factorial(self, element):    # Definition the factorial function.
        product = 1
        for i in range(1, element+1): # Range is from 1 and needs to be incremented by 1 to include the limit
            product *= i
        
        return product


#### main execution section of the program #####
 
print 'Starting the main thread at: ', ctime()          # Recording the time when we started the main thread.
 
while(SOURCE_INPUT_POS < len(sourceInput)):
    MyThread(sourceInput[SOURCE_INPUT_POS]).start()     # Create a new thread for each element of the source list.
    
    sleep(random.random()* 5)                           # Random sleep time to slow down the operations of the threads so we can see 
                                                        # what is happening. 
 
print 'The computed output: \n', sourceOutput           # 
print 'Main thread completed at: ', ctime()             # Recording the time when we finished executing the threads.
