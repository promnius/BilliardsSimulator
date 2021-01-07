

import matplotlib.pyplot as plt # for plotting.
import math

"""This class contains the tools for making a fixed plot that helps visualize a pool break by plotting each timestep for each
ball as a separate point. great for debugging because you can easily identify where the ODE solver felt more/less points were necessary,
but can be very confusing to interpret for large numbers of balls."""
class Plot_Drawing():
    
    def __init__(self):
        pass
    
    """This method takes an input of balls and walls and plots them. as the only method, with no class level variables, this could very well
    just be a function. It was implemented as a method of a class to give future functionality, when all of the different visualization methods
    may become part of the same class. """
    def draw(self, ball_list, wall_list):
        plt.figure()
        
        # calculating the appropriate max/ min display.
        # we are assuming that no balls are outside of the border to start with. if they are, things
        # will not work correctly (they won't be able to get inside), and they may not be displayed
        left = wall_list[0][0]
        right = wall_list[0][0]
        top = wall_list[0][1]
        bottom = wall_list[0][1]
        # find the extremes
        for counter in range(0, len(wall_list)):
            x = wall_list[counter][0]
            y = wall_list[counter][1]
            if x > right:
                right = x
            if x < left:
                left = x
            if y > top:
                top = y
            if y < bottom:
                bottom = y
                
        # expanding borders slightly so that pockets are on screen
        width_cushioning = math.fabs(left - right) * .1 # arbitrarily 10 percent
        height_cushioning = math.fabs(top - bottom) * .1 # arbitrarily 10 percent
        top += height_cushioning
        bottom -= height_cushioning
        left -= width_cushioning
        right += width_cushioning
        # setting borders      
        ax = plt.axes(xlim = [left, right], 
                    ylim = [bottom, top])
        # making sure that the aspect ratio is not affected by the window size, which would make
        # the pool table look distorted.
        ax.set_aspect('equal', adjustable='box')
        
        # plotting the boundry
        for counter in range(1,len(wall_list)):
            # extracting the x,y coordinates of the next line
            x = [(wall_list[counter - 1][0]), (wall_list[counter][0])]
            y = [(wall_list[counter - 1][1]), (wall_list[counter][1])]
            plt.plot(x,y, 'b', linewidth=5)
        # deal with connecting the last line to the first
        x = [(wall_list[counter][0]), (wall_list[0][0])]
        y = [(wall_list[counter][1]), (wall_list[0][1])]
        plt.plot(x,y, 'b', linewidth=5)
        
        # now make the plot!
        # plot the ball positions
        symbol_type = ['x','o']
        color_type = ['b', 'r', 'g']
        for ball_counter in range(len(ball_list)):
            symbol = ball_counter % len(symbol_type)
            color = ball_counter / len(symbol_type)
            color = color % len(color_type)
            setup_string = color_type[color] + symbol_type[symbol]
            ball = ball_list[ball_counter]
            plt.plot(ball.position_x_record, ball.position_y_record, setup_string)
        
        plt.show()


