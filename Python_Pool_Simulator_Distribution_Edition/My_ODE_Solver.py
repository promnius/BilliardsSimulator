

"""This is a first order ODE solver used to integrate the positions of balls. Higher orders are not necessary, due to the
simple nature of the differential equations that govern the physics of the balls. The reason I chose to write my own ODE solver
is because every impact is an event that must be handled separately, and during the break there may be thousands of these events.
My ODE solver integrates the impact solver into itself, to make event handling more fluid. Other features: it does dynamic timestep
allocation and recursive timestep refinement around impacts."""
class ODE_Solver():
    
    max_loops = 150 # arbitrary, the maximum number of iterations. Ideally, it is selected such that
    # no ball can have this number of steps and not hit something or stop. Realistically, this is the number of steps before
    # the size of the timestep is re-evaluated, assuming no impact. too large and the timestep may not be optimized, too
    # small and computation time will be wasted re-evaluating an acceptable timestep.
    def __init__(self):
        pass
        
    """This method continues to update the positions of balls until an impact is found. then it recursively refines the timestep
    at this point, and solves the impact. It then returns so that the situation can be re-analyzed (did any balls hit a pocket?
    stop moving?)"""
    def solve_till_impact(self, ball_list, wall_points, crash, current_depth= 0, time_step= None):
        if len(ball_list) == 0:
            return "ALL_BALLS_STATIONARY"
        
        # calculate timestep. The requirements for an ideal timestep are based off of 
        # collisions, since larger timesteps and you could miss a collision, smaller 
        # and you waste time. I decided to calculate a timestep every 1/4 of the ball diameter
        # note that an override can be supplied by the function (used primarily for recursion)
        
        # time step should be in seconds
        # NOTE: no error checking performed. an unacceptable input given by the user will result in bad errors.
        
        # in future iterations, I may (depending on processing power) add intermediate
        # steps to allow greater precision; slight alteration of the code would be required. One scenario
        # where this would be desirable is if spin is added to the physics.     
        if time_step == None:
            fastest_ball = self.max_ball_velocity(ball_list) # should be in meters per second
            if fastest_ball.current_speed() == 0:
                # the fact that this is detected here, and not during the iteration loop, means that a ball (the last one moving!) was probably just sunk.
                return "ALL_BALLS_STATIONARY"
            time_step = fastest_ball.ball_diameter/(4 * fastest_ball.current_speed())
            # debugging
            #print "" # just to give an extra blank line before each round of ODE.
            #print "time step used for this round of ODE: " + str(time_step) + " seconds"
        else:
            # debugging
            #print "time step reduced to: " + str(time_step) + "seconds"
            pass # time step defined by user, no action required


        not_done = True
        infinite_loop_counter = 0 # to stop an infinite loop. also for determining when it is time to re-assess timestep size.
        
        # continue to move balls until an end condition is met        
        while not_done:
            # move balls
            for ball in ball_list:
                ball.advance_position(time_step)            
            
            # check if done
            # if every ball has stopped moving, we are done.
            not_moving = True
            for ball in ball_list:
                # looking at velocity x and velocity y
                if ball.current_speed() > 0:
                    not_moving = False # at least one ball is still moving
            # debugging
            if not_moving:
                pass
                #print "end condition reached: balls are not moving."
            
            # if a collision has occured, we are done, but probably need to refine more. RECURSION!!
            impact = False
            impact_return = crash.check_for_large_contact()
            if impact_return != 3:
                # debugging- some form of impact detected!
                pass
            if impact_return == 1:
                # impact was too great. back up. recursively refine timestep.
                for ball in ball_list:
                    ball.remove_last_state_point()
                if current_depth > 20:
                    # great for catching an infinite recursion. precision less than (1/2^20) should never be required
                    print "NOT GOOD!! infinite recursion detected!?!" 
                    return "ALL_BALLS_STATIONARY"
                else:
                    motion = self.solve_till_impact(ball_list, wall_points, crash, time_step = time_step/2, current_depth = current_depth + 1)
                    if motion == "ALL_BALLS_STATIONARY":
                        return "ALL_BALLS_STATIONARY"
                
                # now the final points have an acceptably small amount of impact overlap.
                impact = True
            elif impact_return == 2:
                # impact is perfect. please stop.
                impact = True
                # debugging 
                #print "end condition reached: impact detected and recursively solved."
            else:
                # no impact. continue.
                pass

            # now all the calculations for the current timestep have been completed. Check for any critical events.
            if impact:
                pass
                # debugging
                # print "end condition reached: there was an impact"
            if infinite_loop_counter > self.max_loops:
                pass
                # debugging
                #print "end condition reached: timeout. infinite loop detected? or just ready for timestep re-assessment. exiting ODE solver."
                #print "It is possible that the balls are moving very slow. Will try again with coarser step."
            if impact or not_moving or infinite_loop_counter > self.max_loops:
                not_done = False
            infinite_loop_counter += 1
        
        # loop exited. some exit condition met.
        if not_moving:
            return "ALL_BALLS_STATIONARY"
        elif impact:
            return "IMPACT_DETECTED"
        elif infinite_loop_counter> self.max_loops:
            return "TIME_OUT_ERROR"
        else: # unidentified error
            return "UNIDENTIFIED_ERROR"            
    
    """This method returns the fastest ball from a list of balls. This is helpful in calculating the appropriate timestep."""
    def max_ball_velocity(self, ball_list):
        # maybe a faster method, but this next line isn't working correctly
        max_speed = 0
        for counter in range(0, len(ball_list)):
            if ball_list[counter].current_speed() >= max_speed:
                max_speed = ball_list[counter].current_speed()
                fastest_ball_index = counter
        return ball_list[fastest_ball_index]
        
    