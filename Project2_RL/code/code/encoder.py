import random,argparse,sys
parser = argparse.ArgumentParser()
import numpy as np

def convertToTwoDigit (number):
    if number < 10:
        return str('0') + str(number)
    else :
        return number
    

def tacklePosition (transitions, B1, B2, R, pos, cur, j):
    
    
    
def checkOutofBoundsB1 (B1, B2, R, pos, transitions, rewards, cur, j, P):
    R = convertToTwoDigit (R)
    final_state = B1 + B2 + R + pos

    if (int(B1) == 0):
        transitions[cur][j][final_state] = 1
        rewards[cur][j][final_state] = 0

    elif (B1 == R or int(R) < int(B1)):
        tacklePosition (transitions)

    else :
        transitions[cur][j][final_state] = P
        rewards[cur][j][final_state] = 0

def checkOutofBoundsB2 (B1, B2, R, pos, transitions, rewards, cur, j, P):
    R = convertToTwoDigit (R)
    final_state = B1 + B2 + R + pos

    if (int(B2) == 0):
        transitions[cur][j][final_state] = 1
        rewards[cur][j][final_state] = 0

    elif (B2 == R or int(R) < int(B2)):
        tacklePosition (transitions)

    else :
        transitions[cur][j][final_state] = P
        rewards[cur][j][final_state] = 0


def readOpponentFile ( file_path ):
    with open(file_path, 'r') as file:
        total_actions = 10
        total_states = 8092
        transitions = np.zeros((total_states, 
                    total_actions, total_states), dtype=np.float64)
        rewards = np.zeros((total_states, 
                    total_actions, total_states), dtype=np.float64)
        
        i = 0
        for line in file:
            words = line.split()
            if (i > 0):

                current_state = words[0]
                P_L = float(words[1])
                P_R = float(words[2])
                P_U = float(words[3])
                P_D = float(words[4])

                for j in range(total_actions):

                    B1 = current_state[:2]
                    B2 = current_state[2:4]
                    R = int(current_state[4:6])
                    possesion = current_state[6]


                    if j < 4:
                        B1_new = int(B1)
                        if j == 0 :
                            B1_new = B1_new - 1
                            if ( B1_new % 4 == 0):
                                B1_new = 0
                        elif j == 1:
                            B1_new = B1_new + 1
                            if ( B1_new % 4 == 1):
                                B1_new = 0
                        elif j == 2:
                            B1_new = B1_new - 4
                            if ( B1_new < 1):
                                B1_new = 0
                        else :
                            B1_new = B1_new + 4
                            if ( B1_new > 16):
                                B1_new = 0

                        B1_new = convertToTwoDigit (B1_new)

                        R_new = R - 1
                        checkOutofBoundsB1 (B1_new, B2, R_new, possesion, transitions, rewards, current_state, j, P_L)

                        R_new = R + 1
                        checkOutofBoundsB1 (B1_new, B2, R_new, possesion, transitions, rewards, current_state, j, P_R)

                        R_new = R - 4
                        checkOutofBoundsB1 (B1_new, B2, R_new, possesion, transitions, rewards, current_state, j, P_U)

                        R_new = R + 4
                        checkOutofBoundsB1 (B1_new, B2, R_new, possesion, transitions, rewards, current_state, j, P_D)

                    elif j < 8 :
                        B2_new = int(B2)
                        if j == 0 :
                            B2_new = B2_new - 1
                            if ( B2_new % 4 == 0):
                                B2_new = 0
                        elif j == 1:
                            B2_new = B2_new + 1
                            if ( B2_new % 4 == 1):
                                B2_new = 0
                        elif j == 2:
                            B2_new = B2_new - 4
                            if ( B2_new < 1):
                                B2_new = 0
                        else :
                            B2_new = B2_new + 4
                            if ( B2_new > 16):
                                B2_new = 0

                        B2_new = convertToTwoDigit (B2_new)

                        R_new = R - 1
                        checkOutofBoundsB2 (B1, B2_new, R_new, possesion, transitions, rewards, current_state, j, P_L)
                        R_new = R + 1
                        checkOutofBoundsB2 (B1, B2_new, R_new, possesion, transitions, rewards, current_state, j, P_R)
                        R_new = R - 4
                        checkOutofBoundsB2 (B1, B2_new, R_new, possesion, transitions, rewards, current_state, j, P_U)
                        R_new = R + 4
                        checkOutofBoundsB2 (B1, B2_new, R_new, possesion, transitions, rewards, current_state, j, P_D)

                    elif j == 8:
                        



                        



def __init__ (self, states, actions, trasitions):



def generateFootballMDP ( self):
    print("numSates", self.total_states)
    print("numActions",self.total_actions)

    for i in range(self.endArray):
        print('end' + self.endArray[i] + " ")
    
    for trans in self.transitionArray:
        print("transition" + str(self.transitionArray[0]) + ' ' + 
              str(self.transitionArray[1]) + ' '+ str(self.transitionArray[2]))


    print("mdptype",self.mdptype)
    print("discount ",self.gamma)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--opponent", help="Path to the opponent policy file")
    parser.add_argument("--p", type=float)
    parser.add_argument("--q", type=float)
    args = parser.parse_args()
    
    readOpponentFile( args.opponent)
    

    
    