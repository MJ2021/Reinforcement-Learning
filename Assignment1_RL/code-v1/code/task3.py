"""
NOTE: You are only allowed to edit this file between the lines that say:
    # START EDITING HERE
    # END EDITING HERE

This file contains the FaultyBanditsAlgo class. Here are the method details:
    - __init__(self, num_arms, horizon, fault): This method is called when the class
        is instantiated. Here, you can add any other member variables that you
        need in your algorithm.
    
    - give_pull(self): This method is called when the algorithm needs to
        select an arm to pull. The method should return the index of the arm
        that it wants to pull (0-indexed).
    
    - get_reward(self, arm_index, reward): This method is called just after the 
        give_pull method. The method should update the algorithm's internal
        state based on the arm that was pulled and the reward that was received.
        (The value of arm_index is the same as the one returned by give_pull.)
"""

import numpy as np
import math

# START EDITING HERE
# You can use this space to define any helper functions that you need
# END EDITING HERE

class FaultyBanditsAlgo:
    def __init__(self, num_arms, horizon, fault):
        # You can add any other variables you need here
        self.num_arms = num_arms
        self.horizon = horizon
        self.fault = fault # probability that the bandit returns a faulty pull
        self.counts = np.zeros(num_arms)
        self.values = np.zeros(num_arms)
        self.empmean = np.zeros(num_arms)
        self.time = 1
        # START EDITING HERE

        # END EDITING HERE
    
    def give_pull(self):
        # START EDITING HERE
        # raise NotImplementedError
        # max_ucb = 0
        # index = 0
        # for i in range(0, len(self.counts)):
        #     if (self.counts[i] == 0):
        #         return i
        # for i in range(0, len(self.counts)):  
        #     ucb = self.empmean[i] + math.sqrt((2*math.log(self.time))/self.counts[i])
        #     if ( ucb > max_ucb ):
        #         index = i
        #         max_ucb = ucb
        # return index


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
        self.time += 1
        self.values[arm_index] += reward
        self.empmean[arm_index] = self.values[arm_index]/self.counts[arm_index]
        #END EDITING HERE

