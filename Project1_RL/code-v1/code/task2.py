"""
You need to write code to plot the graphs as required in task2 of the problem statement:
    - You can edit any code in this file but be careful when modifying the simulation specific code. 
    - The simulation framework as well as the BernoulliBandit implementation for this task have been separated from the rest of the assignment code and is contained solely in this file. This will be useful in case you would like to collect more information from runs rather than just regret.
"""

import numpy as np
from multiprocessing import Pool
from task1 import Eps_Greedy, UCB, KL_UCB
import matplotlib.pyplot as plt
import time
# START EDITING HERE
# You can use this space to define any helper functions that you need.
# END EDITING HERE

class BernoulliArmTask2:
  def __init__(self, p):
    self.p = p

  def pull(self, num_pulls=None):
    return np.random.binomial(1, self.p, num_pulls)

class BernoulliBanditTask2:
  def __init__(self, probs=[0.3, 0.5, 0.7],):
    self.__arms = [BernoulliArmTask2(p) for p in probs]
    self.__max_p = max(probs)
    self.__regret = 0

  def pull(self, index):
    reward = self.__arms[index].pull()
    self.__regret += self.__max_p - reward
    return reward

  def regret(self):
    return self.__regret
  
  def num_arms(self):
    return len(self.__arms)


def single_sim_task2(seed=0, ALGO=Eps_Greedy, PROBS=[0.3, 0.5, 0.7], HORIZON=1000):
  np.random.seed(seed)
  np.random.shuffle(PROBS)
  bandit = BernoulliBanditTask2(probs=PROBS)
  algo_inst = ALGO(num_arms=len(PROBS), horizon=HORIZON)
  for t in range(HORIZON):
    arm_to_be_pulled = algo_inst.give_pull()
    reward = bandit.pull(arm_to_be_pulled)
    algo_inst.get_reward(arm_index=arm_to_be_pulled, reward=reward)
  return bandit.regret()

def simulate_task2(algorithm, probs, horizon, num_sims=50):
  """simulates algorithm of class Algorithm
  for BernoulliBandit bandit, with horizon=horizon
  """
  
  def multiple_sims(num_sims=50):
    with Pool(10) as pool:
      sim_out = pool.starmap(single_sim_task2,
        [(i, algorithm, probs, horizon) for i in range(num_sims)])
    return sim_out 

  sim_out = multiple_sims(num_sims)
  regrets = np.mean(sim_out)

  return regrets

def task2(algorithm, horizon, p1s, p2s, num_sims=50):
    """generates the data for task2
    """
    probs = [[p1s[i], p2s[i]] for i in range(len(p1s))]

    regrets = []
    for prob in probs:
        regrets.append(simulate_task2(algorithm, prob, horizon, num_sims))

    return regrets

if __name__ == '__main__':
  # EXAMPLE CODE
  task2p1s = [0.2, 0.3]
  task2p2s = [0.1, 0.2]
  regrets = task2(Eps_Greedy, 1000, task2p1s, task2p2s, 50)
  print(regrets)
  # INSERT YOUR CODE FOR PLOTTING HERE

  task2p1_ucb = []
  task2p2_ucb = []
  for i in np.arange(0, 0.95, 0.05):
    task2p1_ucb.append(0.9)
    task2p2_ucb.append(i)
  regrets_ucb = task2(UCB, 30000, task2p1_ucb, task2p2_ucb, 50)
  print(regrets_ucb)

  plt.plot(task2p2_ucb, regrets_ucb)
  plt.title("Regret vs P2")
  plt.savefig("task2-{}-{}.png".format("UCB-", time.strftime("%Y%m%d-%H%M%S")))
  plt.clf()

  task2b_p1 = []
  task2b_p2 = []
  for i in np.arange(0, 0.95, 0.05):
    task2b_p1.append(i + 0.1)
    task2b_p2.append(i)

  regrets_ucb_p2 = task2(UCB, 30000, task2b_p1, task2b_p2, 50)
  regrets_klucb = task2(KL_UCB, 30000, task2b_p1, task2b_p2, 50)

  print(regrets_ucb_p2)
  print(regrets_klucb)

  plt.plot(task2b_p2, regrets_ucb_p2)
  plt.title("UCB Regret vs P2")
  plt.savefig("task2b-{}-{}.png".format("UCB-", time.strftime("%Y%m%d-%H%M%S")))
  plt.clf()

  plt.plot(task2b_p2, regrets_klucb)
  plt.title("KL UCB Regret vs P2")
  plt.savefig("task2b-{}-{}.png".format("KL-UCB", time.strftime("%Y%m%d-%H%M%S")))
  plt.clf()


  pass