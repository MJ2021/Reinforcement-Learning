"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the base Algorithm class that all algorithms should inherit
from. Here are the method details:
    - __init__(self, num_arms, horizon): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)

We have implemented the epsilon-greedy algorithm for you. You can use it as a
reference for implementing your own algorithms.
"""

import numpy as np
import math
# Hint: math.log is much faster than np.log for scalars

class Algorithm:
    def __init__(self, num_arms, horizon):
        self.num_arms = num_arms
        self.horizon = horizon
    
    def give_pull(self):
        raise NotImplementedError
    
    def get_reward(self, arm_index, reward):
        raise NotImplementedError

# Example implementation of Epsilon Greedy algorithm
class Eps_Greedy(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # Extra member variables to keep track of the state
        self.eps = 0.1
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
    
    def give_pull(self):
        if np.random.random() < self.eps:
            return np.random.randint(self.num_arms)
        else:
            return np.argmax(self.values)
    
    def get_reward(self, arm_index, reward):
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        value = self.values[arm_index]
        new_value = ((n - 1) / n) * value + (1 / n) * reward
        self.values[arm_index] = new_value

# START EDITING HERE
# You can use this space to define any helper functions that you need
def kl_divergence(x, y):
    if (x == y):
        return 0
    if (x == 0) :
        x += 1e-10
    elif (x >= 1):
        x = 1 - 1e-10
    if (y == 0):
        y += 1e-10
    elif (y >= 1):
        y = 1 - 1e-10
    return x*math.log(x/y) + (1-x)*math.log((1-x)/(1-y))
# END EDITING HERE

class UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.empmean = np.zeros(num_arms)
        self.time = 1
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        # raise NotImplementedError
        max_ucb = 0
        index = 0
        for i in range(0, len(self.counts)):
            if (self.counts[i] == 0):
                return i
        for i in range(0, len(self.counts)):  
            ucb = self.empmean[i] + math.sqrt((2*math.log(self.time))/self.counts[i])
            if ( ucb > max_ucb ):
                index = i
                max_ucb = ucb
        return index

        # END EDITING HERE  
        
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        # raise NotImplementedError
        self.counts[arm_index] += 1
        self.time += 1
        self.values[arm_index] += reward
        self.empmean[arm_index] = self.values[arm_index]/self.counts[arm_index]
        # END EDITING HERE


class KL_UCB(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.empmean = np.zeros(num_arms)
        self.time = 1
        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        # raise NotImplementedError
        q_max = 0
        index = 0

        for i in range(0, len(self.counts)):
            if (self.counts[i] == 0):
                return i
            
        log_time = math.log(self.time)
        for i in range(0, len(self.counts)):
            q_prev = self.empmean[i]
            q = q_prev
            q_next = 1
            count = 0
            while ((abs(q_prev - q_next) >= 1e-4) or count == 0) :
                count += 1
                if (self.counts[i]*kl_divergence(self.empmean[i], q) <= log_time + 0*np.log(log_time)) :
                    if (q > q_max) :
                        index = i
                        q_max = q
                    q_prev = q
                    q = (q + q_next)/2
                else :
                    q_next = q
                    q = (q + q_prev)/2

        return index
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        # raise NotImplementedError
        self.counts[arm_index] += 1
        self.time += 1
        self.values[arm_index] += reward
        self.empmean[arm_index] = self.values[arm_index]/self.counts[arm_index]
        # END EDITING HERE

class Thompson_Sampling(Algorithm):
    def __init__(self, num_arms, horizon):
        super().__init__(num_arms, horizon)
        # You can add any other variables you need here
        # START EDITING HERE
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)

        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        # raise NotImplementedError
        max_sample = 0
        index = 0
        for i in range(0, len(self.counts)):
            if (self.counts[i] == 0):
                return i
            
        for i in range(0, len(self.counts)):
            sample = np.random.beta(self.values[i]+1, self.counts[i] - self.values[i] +1)
            if (sample > max_sample):
                index = i
                max_sample = sample
        return index
        # END EDITING HERE
    
    def get_reward(self, arm_index, reward):
        # START EDITING HERE
        # raise NotImplementedError
        self.counts[arm_index] += 1
        self.values[arm_index] += reward
        # END EDITING HERE
