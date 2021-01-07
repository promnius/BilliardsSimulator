

import math

"""This class models a physical pool ball. It holds state information for this ball, as well as provides methods
for updating state."""
class Pool_Balls():
    
    # constants
    mu_sliding = .2 # coefficient of friction sliding
    mu_rolling = .03 # much smaller, because rolling == low friction. Numbers estimated using online sources.
    mu_ball_to_ball = .05 # not used in current model- collisions are handled as instant events using restitution.
    g = 9.8 # meters per second per second
    ball_diameter = .05715 # meters
    
    """Initializes a ball with no previous record of motion and no current velocity."""
    def __init__(self, x_position, y_position, cue_ball_or_not):
        self.clear_state()
        
        # initialize a new ball
        self.position_x_record.append(x_position)
        self.position_y_record.append(y_position)
        self.velocity_x_record.append(0)
        self.velocity_y_record.append(0)
        self.time_record.append(0)
        
        if cue_ball_or_not == "CUE_BALL":
            # ball is a cue ball
            self.ball_mass = .17 # in kilograms
            self.is_cue_ball = True
        elif cue_ball_or_not == "NOT_CUE_BALL":
            # ball is not a cue ball
            self.ball_mass = .16 # in kilograms
            self.is_cue_ball = False
        else:
            # error, wrong entry
            print "Ball type does not exist. Assuming the ball is not a cue ball. Error code 29582793."
            self.ball_mass = .16 # in kilograms
            self.is_cue_ball = False
    
    """this method returns the current speed (NOT velocity)"""
    def current_speed(self):
        end = len(self.velocity_x_record) - 1
        return math.sqrt(self.velocity_x_record[end]**2 + self.velocity_y_record[end]**2)
    
    """Updates the status of the ball by appending a new position and velocity to the end of the state vectors."""
    def add_state_point(self, time, positionx, positiony, velocityx, velocityy):
        self.position_x_record.append(positionx)
        self.position_y_record.append(positiony)
        self.velocity_x_record.append(velocityx)
        self.velocity_y_record.append(velocityy)
        self.time_record.append(time)
    
    """Removes the last state of the ball. Useful for recursively refining collisions, since an ODE solver may overshoot
    the event location."""
    def remove_last_state_point(self):
        self.position_x_record.pop()
        self.position_y_record.pop()
        self.velocity_x_record.pop()
        self.velocity_y_record.pop()
        self.time_record.pop()
        
    """Completely wipes the balls record. Useful for initializing a new ball, or clearing the ball's history to play a new game.
    (or a new break)"""
    def clear_state(self):
        self.position_x_record = []
        self.position_y_record = []
        self.velocity_x_record = []
        self.velocity_y_record = []
        self.time_record = []        
 
    """This method uses the differential equations of motion (very simple for this model) to estimate the position of the ball after 
    a given timestep. it then appends this new location to the end of the state vectors. """   
    def advance_position(self, timestep):
        # calculate the differentials using the last known state vector
        differentials = self.differential_equations()
        
        # temporarily record last state
        end = len(self.position_x_record) - 1
        last_p_x = self.position_x_record[end]
        last_p_y = self.position_y_record[end]
        last_v_x = self.velocity_x_record[end]
        last_v_y = self.velocity_y_record[end]
        
        # breakout differentials vector
        diff_p_x = differentials[0]
        diff_p_y = differentials[1]
        diff_v_x = differentials[2]
        diff_v_y = differentials[3]
        
        # calculate new states. Multiply differentials by timestep to get new state vector
        new_p_x = last_p_x + diff_p_x * timestep
        new_p_y = last_p_y + diff_p_y * timestep
        new_v_x = last_v_x + diff_v_x * timestep
        new_v_y = last_v_y + diff_v_y * timestep
        new_time = self.time_record[end] + timestep
        
        # checking if either of the velocitys has crossed zero- this
        # is a bad thing, and occurs as an artifact of Eulers method. I set the velocity to zero when this occurs
        if self.same_sign(new_v_x, last_v_x) == False: # zero point was crossed, new velocity should be 0
            new_v_x = 0
        if self.same_sign(new_v_y, last_v_y) == False:
            new_v_y = 0
        
        # update states
        self.add_state_point(new_time, new_p_x, new_p_y, new_v_x, new_v_y)

    """This method returns the differential equations of motion for a ball, based on the physics modeling decisions
    for this project. """
    def differential_equations(self):
        end = len(self.position_x_record) - 1
        # breakout state vector
        velocityx = self.velocity_x_record[end]
        velocityy = self.velocity_y_record[end]
        
        # determine the correct mu to use
        if self.current_speed() > 2: # for high speeds, the ball will slide rather than roll. Number selected
            # based on an average of multiple online sources.
            friction = self.mu_sliding
        else:
            friction = self.mu_rolling
        
        # calculates the equations used in differential solvers.
        dpxdt = velocityx
        dpydt = velocityy
        
        # avoiding a divide by zero error
        if velocityx == 0 and velocityy == 0:
            dvxdt = 0
            dvydt = 0
        else:
            dvxdt = - (friction * self.g * velocityx)/ (math.sqrt(velocityx**2 + velocityy**2))
            dvydt = - (friction * self.g * velocityy)/ (math.sqrt(velocityx**2 + velocityy**2))
        
        return [dpxdt, dpydt, dvxdt, dvydt]

    """This method returns true if x,y are the same sign, false otherwise. useful for checking if two points have crossed zero."""
    def same_sign(self, x, y):
        if x > 0:
            if y < 0: # signs are different
                return False
        elif x < 0:
            if y > 0: # signs are different
                return False
        else:
            # one number may be zero, but that is ok.
            return True
        
        