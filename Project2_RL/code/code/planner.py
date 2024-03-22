import numpy as np 
import argparse
from pulp import *

class METHODS():
    def __init__(self, total_states, total_actions, transitions, rewards, type_mdp, gamma):
        self.total_states = total_states
        self.total_actions = total_actions
        self.transitions = transitions
        self.rewards = rewards
        self.type_mdp = type_mdp
        self.gamma = gamma

    def valueFunction (self, policy_taken):

        value = np.zeros(self.total_states)
        actual_value = np.zeros(self.total_states)

        while(1):
            actual_value = np.zeros(self.total_states)
            for s in range(self.total_states):
                for s_dash in range(self.total_states):
                    actual_value[s] += self.transitions[s][ int(policy_taken[s]) ][s_dash]*(self.rewards[s][ int(policy_taken[s]) ][s_dash] + self.gamma * value[s_dash])
            if (np.linalg.norm(actual_value - value)< 1e-12):
                break
            else:
                value = actual_value
        return actual_value


    def activeValueFunction (self, V):
        avf = np.zeros((self.total_states, self.total_actions))
        for s in range(self.total_states):
            for a in range(self.total_actions):
                for s_dash in range(self.total_states):
                    avf[s][a] += self.transitions[s][a][s_dash] * (self.rewards[s][a][s_dash] + self.gamma *  V[s_dash])

        return avf


    def bellmanOptimalityOperator (self, current_value):
        optimal_value = np.zeros( self.total_states)
        optimal_actions = np.zeros( self.total_states)
        optimal_action = 0
        for s in range(self.total_states):
            max_value = 0
            for a in range(self.total_actions):
                new_value = 0
                for s_dash in range(self.total_states):
                    new_value += self.transitions[s][a][s_dash]*(self.rewards[s][a][s_dash] + self.gamma * current_value[s_dash])
                if (new_value >= max_value):
                    max_value = new_value
                    optimal_action = a
            optimal_actions[s] = optimal_action
            optimal_value[s] = max_value
        
        return optimal_value, optimal_actions

    def valueIteration (self):
        V_old = np.zeros( self.total_states)
        threshold = 1e-10
        V_new = np.ones( self.total_states)
        while(np.linalg.norm(V_new -V_old) > threshold ):
            V_old = V_new
            V_new, Optimal_policy = self.bellmanOptimalityOperator(V_old)

        return V_new, Optimal_policy

    def linearProgramming (self):

        problem = LpProblem('Linear_Programming', LpMinimize)
        V = np.array(list(LpVariable.dicts("Values", [i for i in range(self.total_states)]).values()))
        problem += lpSum(V)  
        for s in range(self.total_states):
            for a in range(self.total_actions):
                intermediate_value = 0.0
                for s_dash in range(self.total_states):
                    intermediate_value += (self.transitions[s][a][s_dash] * ( self.rewards[s][a][s_dash] + self.gamma * V[s_dash]))
                problem += V[s] >= intermediate_value

        problem.solve(apis.PULP_CBC_CMD(msg=False))
        new_value = np.zeros((self.total_states,1))
        for i in range(self.total_states):
            new_value[i,0] = V[i].value()

        new_value = new_value.reshape((1,1,self.total_states))
        
        policy = np.argmax(np.sum(self.transitions * (self.rewards + self.gamma * new_value), axis=-1), axis=-1)
        new_value = new_value.reshape(self.total_states)
        return new_value, policy


    def howardPolicyIteration (self):

        policy = np.zeros((self.total_states), dtype=int)
        while(1):
            value = self.valueFunction(policy)
            avf = self.activeValueFunction(value)
            improvable_actions = np.amax(avf, axis = 1) - value
            if np.amax(improvable_actions) < 1e-10:
                break
            new_policy = np.argmax(avf, axis = 1)
            for i in range(len(improvable_actions)):
                if (improvable_actions[i] >= 1e-10):
                    policy[i] = new_policy[i]

        return value, policy

    
def readMDPFile (file_path):
    #Initialize a NumPy 3D array with zeros
    # transitions = np.zeros((8194, 10, 8194), dtype=np.float64)
    # rewards = np.zeros((8194, 10, 8194), dtype=np.float64)
    with open(file_path, 'r') as file:
        for line in file:
            words = line.split()
            if words[0] == 'numStates':
                total_states = int(words[1])

            elif words[0] == 'numActions':
                total_actions = int(words[1])
                transitions = np.zeros((total_states, total_actions, total_states), dtype=np.float64)
                rewards = np.zeros((total_states, total_actions, total_states), dtype=np.float64)

            elif words[0] == 'transition':
                initial_state = int(words[1])
                action_taken = int(words[2])
                final_state = int(words[3])
                transitions[initial_state][action_taken][final_state] = float(words[5])
                rewards[initial_state][action_taken][final_state] = float(words[4])

            elif words[0] == 'mdptype':
                type_mdp = words[1]

            elif words[0] == 'discount':
                gamma = float(words[1])

    return total_states, total_actions, transitions, rewards, type_mdp, gamma


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp", help="Path to the mdp file")
    parser.add_argument("--algorithm", choices = ['vi', 'hpi', 'lp'], \
        help="Value Iteration, Howard Policy Iteration, Linear Programming", default="vi")
    parser.add_argument("--policy", help="Path to the mdp file", default = None)

    args = parser.parse_args()

    total_states, total_actions, transitions, rewards, type_mdp, gamma = readMDPFile(args.mdp)
    
    task1 = METHODS(total_states, total_actions, transitions, rewards, type_mdp, gamma)
    
    if (args.policy != None):
        file_path = args.policy
        policy_taken = np.zeros(total_states)
        with open(file_path, 'r') as file:
            i = 0
            for line in file:
                words = line.split()
                policy_taken[i] = words[0]
                i += 1
        V_new = task1.valueFunction(policy_taken)
        Optimal_policy = policy_taken

    elif args.algorithm == 'vi':
        V_new, Optimal_policy = task1.valueIteration()
        
    elif args.algorithm == 'hpi':
        V_new, Optimal_policy = task1.howardPolicyIteration()

    elif args.algorithm == 'lp':
        V_new, Optimal_policy = task1.linearProgramming()

    for i in range(total_states):
            print('%10.7f'%V_new[i]," ",int(Optimal_policy[i]))