
import math

"""This class provides all the functionality for detecting a collision between two balls and solving the collision to create an updated
state vector. The most interesting part is that it keeps track of 'acceptable' distances between each pair of balls (starts as the diameter of a ball),
and shrinks this by the amount those two balls are overlapping every time an impact is solved. this means that after impact, the balls aren't officially
touching anymore, even though they haven't moved anywhere. this is different from most simple pool simulators that solve the overlapping problem by moving the balls
a small amount in their new direction. Moving the balls has the issue that if many pool balls are close together, you may be moving into another one. This is
extremely problematic during a break, which is why my technique was developed. As long as the maximum allowed overlap for a collision is less than .1% of
a ball's diameter (trivial to implement), then even if 2 balls hit each other many times (say 10), no noticeable difference would be noted in the acceptable impact distances. Since
it is unlikely for a specific pair of balls to hit each other many times on a single shot, this technique has turned out to be very successful. """
class Impact_Solver():
    # constants
    max_overlap = .000005715 # should be very small. smaller == more computation time, but more accurate collisions and less calculation drift.
    ball_restitution = .95
    wall_restitution = .6
    #ball_restitution = 1 # for an interesting senario where the balls appear to 'stick' once hitting walls. fairly impractical.
    #wall_restitution = .0001
    
    """Set up the lists of 'acceptable' distances between each pair of balls (and each ball to each wall). they are initialized as
    the ball's diameter (or radius for the acceptable distance to a wall), since if the balls are closer than this they are considered touching."""
    def __init__(self, balls, walls, pockets):
        self.ball_list = balls
        self.wall_list = walls
        self.pocket_list = pockets
        
        # preloading all the minimum distances between balls before impact is detected.
        self.impact_distances = []
        templist = []
        for ball1 in range(0,len(self.ball_list)):
            for ball2 in range(len(self.ball_list)):
                if ball1 < ball2:
                    templist.append(self.ball_list[ball1].ball_diameter/2 + self.ball_list[ball2].ball_diameter/2)

            self.impact_distances.append(templist)
            templist = []
        
        # preloading all the minimum distances between a ball and a wall before impact is detected.
        templist = []    
        self.impact_wall_distances = []
        for ball in range(0,len(self.ball_list)):
            for wall in range(len(self.wall_list)):
                templist.append(self.ball_list[ball].ball_diameter/2)
            self.impact_wall_distances.append(templist)
            templist = []
        # debugging.
        #print "initial impact distances" + str(self.impact_distances)
        #print "initial wall impact distances" + str(self.impact_wall_distances)
        pass
        
    """This method checks for unacceptably large contact between the balls and the walls, indicative of a situation where
    the timesteps need refinement. returns an integer- 1 means there is too much overlap and timestep needs refinement. 2 means
    perfect overlap- time to solve the contact. 3 means no contact- continue as before."""
    def check_for_large_contact(self):
        
        # setting up local variables
        list_balls_touching = []
        list_balls_walls_touching = []
        balls_touching = False
        balls_touching_too_much = False
        balls_touching_wall = False
        ball_sunk = False
        
        # first, check for ball to ball impact
        for iterator in range(0,len(self.ball_list)):
            for iterator2 in range(0,len(self.ball_list)):
                if iterator < iterator2: # we only need to check the impact in one direction
                    ball1 = self.ball_list[iterator]
                    ball2 = self.ball_list[iterator2]
                    end = len(ball1.position_x_record) - 1 # the end should be the same for x and y,
                    # but may be different for different balls if one has stopped moving/ had more/less impacts.
                    X1 = ball1.position_x_record[end]
                    Y1 = ball1.position_y_record[end]
                    end = len(ball2.position_x_record) - 1
                    X2 = ball2.position_x_record[end]
                    Y2 = ball2.position_y_record[end]
                    
                    # check that both balls are still in use
                    if X1 == None or Y1 == None or X2 == None or Y2 == None:
                        # one of the balls has left the table, so obviously there is no interaction
                        pass
                    else:
                        deltaX = math.fabs(X1 - X2)
                        deltaY = math.fabs(Y1 - Y2)
                        distance = math.sqrt(deltaX**2 + deltaY**2)
                        
                        max_impact_distance = self.impact_distances[iterator][(iterator2) - iterator - 1] # more than this and time needs to be backed up.
                        min_impact_distance = max_impact_distance - self.max_overlap # less than this and the balls aren't touching
                        # check if the two balls are too close together, or too far apart
                        if distance > max_impact_distance:
                            # balls are not touching, no action needed
                            pass
                        elif distance > min_impact_distance:
                            # balls are touching perfectly
                            balls_touching = True
                            list_balls_touching.append([iterator, iterator2, distance])
                        else:
                            # balls are overlapping by far too much
                            balls_touching_too_much = True
                            
        # now, check wall to ball contact
        for iterator in range(0,len(self.ball_list)):
            for iterator2 in range(0,len(self.wall_list)):
                ball = self.ball_list[iterator]
                end = len(ball.position_x_record) - 1 # the end should be the same for x and y,
                # but may be different for differen balls if one no longer exists
                X1 = ball.position_x_record[end]
                Y1 = ball.position_y_record[end]
                wall1 = self.wall_list[iterator2]
                if iterator2 < len(self.wall_list) - 1:
                    wall2 = self.wall_list[iterator2+1]
                else:
                    wall2 = self.wall_list[0]
                wall1X = wall1[0]
                wall1Y = wall1[1]
                wall2X = wall2[0]
                wall2Y = wall2[1]     
                
                
                # check that the ball is still in use
                if X1 == None or Y1 == None:
                # the ball has left the table, so obviously there is no interaction
                    pass
                else:
                    px = wall2X-wall1X
                    py = wall2Y-wall1Y
                    temp_dist_sqr = px*px + py*py
                    u =  ((X1 - wall1X) * px + (Y1 - wall1Y) * py) / float(temp_dist_sqr)
                    if u > 1:
                        u = 1
                    elif u < 0:
                        u = 0
                    x = wall1X + u * px
                    y = wall1Y + u * py
                    dx = x - X1
                    dy = y - Y1                
                    # Note: If the actual distance does not matter,
                    # if you only want to compare what this function
                    # returns to other results of this function, you
                    # can just return the squared distance instead
                    # (i.e. remove the sqrt) to gain a little performance
                    distance = math.sqrt(dx*dx + dy*dy)
                    max_impact_distance = self.impact_wall_distances[iterator][iterator2]
                    min_impact_distance = max_impact_distance - self.max_overlap
                    # check if the ball and wall are too close together, or too far apart
                    if distance > max_impact_distance:
                        # ball is not touching wall, no action needed
                        pass
                    elif distance > min_impact_distance:
                        # ball is touching wall perfectly
                        balls_touching_wall = True
                        list_balls_walls_touching.append([iterator, iterator2, distance])
                    else:
                        # ball is overlapping wall by too much
                        balls_touching_too_much = True     
              
        # now, check pockets
        for iterator in range(0,len(self.ball_list)):
            for iterator2 in range(0,len(self.pocket_list)):
                ball = self.ball_list[iterator]
                end = len(ball.position_x_record) - 1
                X1 = ball.position_x_record[end]
                Y1 = ball.position_y_record[end]
                pocket = self.pocket_list[iterator2]
                X2 = pocket[0]
                Y2 = pocket[1]
                # this is a very simple model, but since the diameter of the balls and the diameter of the pockets
                # is pretty fixed, this shouldn't matter too much.
                                 
                # check that the ball is still in use
                if X1 == None or Y1 == None:
                # the ball has left the table, so obviously there is no interaction
                    pass
                else:
                    deltaX = math.fabs(X1 - X2)
                    deltaY = math.fabs(Y1 - Y2)
                    distance = math.sqrt(deltaX**2 + deltaY**2)

                    # check if the ball hit the pocket
                    max_impact_distance = ball.ball_diameter/2 + .5 # where the actual number is the size of the pocket.
                    min_impact_distance = max_impact_distance - self.max_overlap
                    if distance > max_impact_distance:
                        # ball has not hit pocket, no action needed
                        pass
                    elif distance > min_impact_distance:
                        # ball sunk in pocket
                        new_position_x = None
                        new_position_y = None
                        new_velocity_x = 0
                        new_velocity_y = 0
                        time = ball.time_record[end]
                        ball.add_state_point(time, new_position_x, new_position_y, new_velocity_x, new_velocity_y)
                        
                        # debugging
                        #print "BALL SUNK!! CONGRATS!!"
                        ball_sunk = True
                    else:
                        balls_touching_too_much = True
                        
          
        if ball_sunk == True: # do not solve collisions, do not pass go, do not collect $200. deal with this immediately.     
            return 2 # acceptable amount of overlap.
        elif balls_touching_too_much:
            return 1 # too much overlap
        elif balls_touching or balls_touching_wall:
            while list_balls_walls_touching:
                # time to solve the impact.
                
                # debugging.
                # print "Wall impact. Time step sufficiently refined."
                #print "Current list of touching walls (Ball,Wall,distance):" + str(list_balls_walls_touching)
                x,y,distance = list_balls_walls_touching.pop()
                wall1 = self.wall_list[y]
                if y < len(self.wall_list) - 1:
                    wall2 = self.wall_list[y+1]
                else:
                    wall2 = self.wall_list[0]
                wall1X = wall1[0]
                wall1Y = wall1[1]
                wall2X = wall2[0]
                wall2Y = wall2[1]
                if wall2X-wall1X == 0: # wall is vertical, intersection line is horizontal
                    horz_or_vert = 1
                elif wall2Y-wall1Y == 0: # wall is horizontal, intersection line is vertical
                    horz_or_vert = 0
                elif wall2Y > wall1Y and wall2X > wall1X or wall1Y > wall2Y and wall1X > wall2X: # wall is not horizontal or vertical, but
                    # rather 45 degree angle.
                    horz_or_vert = -1
                else: # wall is 45 degrees in the other direction
                    horz_or_vert = -2
                wall_x_vector = wall2X - wall1X
                wall_y_vector = wall2Y - wall1Y
                
                self.find_vel_after_impact_walls(self.ball_list[x], horz_or_vert)
                self.impact_wall_distances[x][y] = distance * .999 # this makes them slightly too far apart so they are 
                # immediately considered not touching.
                
            while list_balls_touching:
                # debugging
                #print "ball-to-ball impact. Time step sufficiently refined."
                #print "Remaining List of touching balls (BallA,BallB,distance):" + str(list_balls_touching)
                x,y,distance = list_balls_touching.pop()
                Ball1 = self.ball_list[x]
                Ball2 = self.ball_list[y]
                self.find_vel_after_impact_with_2d_support(Ball1, Ball2)
                self.impact_distances[x][y-x-1] = distance * .999 # this makes them slightly too far apart so they are 
                # immediately considered not touching.
            return 2 # means that impact level was perfect, and impact was solved.
        else: # nothing is touching
            return 3

    """This method takes a ball and a wall that are touching, and updates the state vector of the ball based on the physics of a 
    collision. """
    def find_vel_after_impact_walls(self, ballA, wall):
        end = len(ballA.velocity_x_record)-1
        # if the wall is horizontal, wall = 0, and the y direction is opposite its initial, while the x direction stays the same
        if wall == 0:
            velocity_1_final_x = ballA.velocity_x_record[end]
            velocity_1_final_y = -ballA.velocity_y_record[end]
            # if the wall is vertical, wall = 1, and the x direction is opposite its inital, while the y direction stays the same
        elif wall == 1:
            velocity_1_final_x = (-ballA.velocity_x_record[end])
            velocity_1_final_y = ballA.velocity_y_record[end]
        elif wall == -1: # walls are at 45
            # wall goes from lower left to upper right
            #print "Wall goes from lower left to upper right"
            Vx = ballA.velocity_x_record[end]
            Vy = ballA.velocity_y_record[end]
            theta = self.calc_theta(Vx, Vy)
            if theta > math.pi/4 and theta < 5 * (math.pi/4):
                # print "ball hit it from above"
                velocity_1_final_x = ballA.velocity_y_record[end]
                velocity_1_final_y = ballA.velocity_x_record[end]
            else:
                # print "ball hit it from below. I don't think a separate solution is needed"
                velocity_1_final_x = ballA.velocity_y_record[end]
                velocity_1_final_y = ballA.velocity_x_record[end]
        else:
            # wall goes from lower right to upper left
            # print "Wall goes from lower right to upper left"
            velocity_1_final_x = - ballA.velocity_y_record[end]
            velocity_1_final_y = - ballA.velocity_x_record[end]
        velocity_1_final_x *= self.wall_restitution
        velocity_1_final_y *= self.wall_restitution
        
        position_1_final_x = ballA.position_x_record[end]
        position_1_final_y = ballA.position_y_record[end]

        time_final = ballA.time_record[end]
        ballA.add_state_point(time_final, position_1_final_x, position_1_final_y, velocity_1_final_x, velocity_1_final_y)

    """This method takes two balls that are touching and updates both of their state vectors based on the physics of a collision. """
    def find_vel_after_impact_with_2d_support(self, BallA, BallB):
        endA = len(BallA.velocity_x_record)-1
        endB = len(BallB.velocity_x_record)-1
        # gets the mass of the first ball from the Ball Class
        mass1 = BallA.ball_mass
        # gets the velocity in the x and y direction of the ball
        U1x = BallA.velocity_x_record[endA]
        U1y = BallA.velocity_y_record[endA]
        U1 = math.sqrt(U1x**2+U1y**2)
       
        # does the same for ball2
        mass2 = BallB.ball_mass
        U2x = BallB.velocity_x_record[endB]
        U2y = BallB.velocity_y_record[endB]
        U2 = math.sqrt(U2x**2+U2y**2)
        
        theta1 = self.calc_theta(U1x, U1y)
        theta2 = self.calc_theta(U2x, U2y)
        
        # calculates phi, the angle between the x axis and the vector through the center of the two balls
        # this is the angle that is used to rotate the coordinate axes.
        # this vector is ball_position_2 - ball_position_1
        P1x = BallA.position_x_record[endA]
        P1y = BallA.position_y_record[endA]
        P2x = BallB.position_x_record[endB]
        P2y = BallB.position_y_record[endB]
        position_vector_x = P2x - P1x
        position_vector_y = P2y - P1y
        phi = self.calc_theta(position_vector_x, position_vector_y)
        
        
        # computes the velocities of both balls in their x and y directions after the impact
        velocity_1_final_x = (U1*math.cos(theta1-phi)*(mass1-mass2)+2*mass2*U2*math.cos(theta2-phi)*math.cos(phi))/(mass1+mass2) + U1*math.sin(theta1-phi)*math.cos(phi+math.pi/2)
        velocity_1_final_y = (U1*math.cos(theta1-phi)*(mass1-mass2)+2*mass2*U2*math.cos(theta2-phi)*math.sin(phi))/(mass1+mass2) + U1*math.sin(theta1-phi)*math.sin(phi+math.pi/2)
        velocity_2_final_x = (U2*math.cos(theta2-phi)*(mass2-mass1)+2*mass1*U1*math.cos(theta1-phi)*math.cos(phi))/(mass1+mass2) + U2*math.sin(theta2-phi)*math.cos(phi+math.pi/2)
        velocity_2_final_y = (U2*math.cos(theta2-phi)*(mass2-mass1)+2*mass1*U1*math.cos(theta1-phi)*math.sin(phi))/(mass1+mass2) + U2*math.sin(theta2-phi)*math.sin(phi+math.pi/2)
        
        position_1_final_x = BallA.position_x_record[endA]
        position_1_final_y = BallA.position_y_record[endA]
        position_2_final_x = BallB.position_x_record[endB]
        position_2_final_y = BallB.position_y_record[endB]
        time_final = BallA.time_record[endA]
        
        velocity_1_final_x *= self.ball_restitution
        velocity_1_final_y *= self.ball_restitution
        velocity_2_final_x *= self.ball_restitution
        velocity_2_final_y *= self.ball_restitution
        
        BallA.add_state_point(time_final, position_1_final_x, position_1_final_y, velocity_1_final_x, velocity_1_final_y)
        BallB.add_state_point(time_final, position_2_final_x, position_2_final_y, velocity_2_final_x, velocity_2_final_y)


    """Given the x and y components of a vector, this function calculates and returns the angle between this vector and the x-axis, 
    using the standard unit circle orientation."""
    def calc_theta(self, Vx, Vy):

        if Vx == 0 and Vy == 0: # singularity, not good.
            theta = 1 # arbitrary. Hopefully it doesn't play into equations
            # debugging
            #print "singularity occurred. hopefully theta doesn't matter!"
        elif Vx > 0:
            theta = math.atan(Vy/Vx)
            if theta < 0:
                theta = theta + 2 * math.pi
        elif Vx < 0:
            theta = math.atan(Vy/Vx) + math.pi
        else: # Vx == 0
            if Vy > 0:
                theta = (math.pi)/2 # 90 degrees
            else: # Vy < 0
                theta = (math.pi/2) + math.pi # 270 degrees
        # debugging
        #print("theta: " + str(theta))
        return theta

                        