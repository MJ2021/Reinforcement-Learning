import os
import sys
import random 
import json
import math
import utils
import time
import config
import numpy
random.seed(73)

class Agent:
    def __init__(self, table_config) -> None:
        self.table_config = table_config
        self.prev_action = None
        self.curr_iter = 0
        self.state_dict = {}
        self.holes =[]
        self.ns = utils.NextState()


    def set_holes(self, holes_x, holes_y, radius):
        for x in holes_x:
            for y in holes_y:
                self.holes.append((x[0], y[0]))
        self.ball_radius = radius

    def distance_angle(self, ball1_x, ball1_y, ball2_x, ball2_y):
        x_distance = ball2_x - ball1_x
        y_distance = ball2_y - ball1_y

        distance = math.sqrt( (x_distance)*(x_distance) + (y_distance)*(y_distance))
        if ( abs( y_distance) < 1e-5 ):
            if ball2_x > ball1_x :
                angle = -0.5
            else :
                angle = 0.5
        elif ( abs ( x_distance) < 1e-5 ):
            if ball2_y < ball1_y :
                angle = 0
            else:
                angle = 1
        elif ( x_distance > 0 and y_distance > 0):
            angle = - (0.5 + ( math.atan ( y_distance / x_distance )) / math.pi)
        elif ( x_distance < 0 and y_distance > 0):
            angle = (0.5 - ( math.atan ( y_distance / x_distance )) / math.pi)
        else :
            angle =   ( math.atan ( x_distance / y_distance )) / math.pi
        return distance, angle


    def action(self, ball_pos=None):
        ## Code you agent here ##
        ## You can access data from config.py for geometry of the table, configuration of the levels, etc.
        ## You are NOT allowed to change the variables of config.py (we will fetch variables from a different file during evaluation)
        ## Do not use any library other than those that are already imported.
        ## Try out different ideas and have fun!

        distance = numpy.zeros(6, dtype = numpy.float64)
        angle = numpy.zeros(6, dtype = numpy.float64)

        distance_holes = numpy.zeros((6,6), dtype = numpy.float64)
        angle_holes = numpy.zeros((6,6), dtype = numpy.float64)

        distances = numpy.zeros(6, dtype = numpy.float64)
        holes = numpy.zeros(6, dtype = numpy.float64)

        white_x = ball_pos[0][0]
        white_y = ball_pos[0][1]

        new_ball = 0

        min_distance_hole = 10000
        min_distance_ball = 0

        for i in ball_pos:
            if ( i == "white"):
                continue
            elif ( i == 0):
                continue

            distance[i], angle[i] = self.distance_angle(white_x, white_y, ball_pos[i][0], ball_pos[i][1])

            for j in range(len(self.holes)):
                distance_holes[i][j], angle_holes[i][j] = self.distance_angle(ball_pos[i][0], ball_pos[i][1], self.holes[j][0], self.holes[j][1])
                if (distance_holes[i][j] < min_distance_hole):
                    min_distance_hole = distance_holes[i][j]
                    min_distance_ball = i

                distances[j], holes[j] = self.distance_angle(white_x, white_y, self.holes[j][0], self.holes[j][1])
            
                if ( abs( angle_holes[i][j] - holes[j]) < 0.1 and distances[j] > distance_holes[i][j]):
                    new_ball = i
                    return (angle[new_ball], 0.75)
        return (angle[min_distance_ball], 1.0 )


        