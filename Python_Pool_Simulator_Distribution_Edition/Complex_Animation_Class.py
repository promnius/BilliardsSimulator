
# known errors: draw method for class Complex_Animation will throw an error if it is handed an empty list.
# this is trivial to solve, but non-critical for this project, as none of these lists will be empty, and 
# furthermore, we would not learn anything from the simulation if they were.

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import math

class Complex_Animation():
    def __init__(self):
        pass
    
    """This method takes a list of balls, walls, and pockets, then generates and displays a movie-like animation of
    a simulated pool shot, using matplotlib's built in animation class. See major known bugs in 'readme' for additional
    issues with the animations. """
    def draw(self, ball_list, wall_list, pocket_list, speed):
        
        # create class scope variables, so that each sub-method can access the instance version and doesn't
        # need to get them passed in.
        self.ball_list = ball_list
        self.wall_list = wall_list
        
        # set up figure and animation
        fig = plt.figure()
    
        # setting borders      
        self.ax = plt.axes(xlim = self.calculate_table_size()[0], 
                           ylim = self.calculate_table_size()[1])
        # making sure that the aspect ratio is not affected by the window size, which would make
        # the pool table look distorted.
        self.ax.set_aspect('equal', adjustable='box')
        
        # calculating the number of frames, assuming 30 frames per seconds. -- so a speed other than
        # 1 will create more or less frames, still played back at 30 frames per second, which will cause the animation to appear
        # faster or slower.
        self.frame_rate = 30
        duration = self.max_time()
        anim_duration = duration/(speed) # in seconds
        num_frames = anim_duration * self.frame_rate
        # adding buffer time at the end and making sure the frame number is an int.
        num_frames = int(num_frames) + 60
        
        # debugging
        print "The duration of the animation is " + str(anim_duration) + " seconds, and we will be using " + str(num_frames) + "frames."
        
        # creating the balls
        self.printable_balls = []
        for ball in self.ball_list:
            off_screen_x = self.calculate_table_size()[0][0] - ball.ball_diameter * 2
            off_screen_y = self.calculate_table_size()[0][1] + ball.ball_diameter * 2
            # note that eventually the color needs to be different for all the different balls.
            patch = plt.Circle((off_screen_x,off_screen_y), radius = (ball.ball_diameter/2), fc='r')
            self.printable_balls.append(patch)
            
        # plotting the boundary
        for counter in range(1,len(wall_list)):
            # extracting the x,y coordinates of the next line
            x = [(wall_list[counter - 1][0]), (wall_list[counter][0])]
            y = [(wall_list[counter - 1][1]), (wall_list[counter][1])]
            plt.plot(x,y, 'b', linewidth=5)
        # deal with connecting the last line to the first
        x = [(wall_list[counter][0]), (wall_list[0][0])]
        y = [(wall_list[counter][1]), (wall_list[0][1])]
        plt.plot(x,y, 'b', linewidth=5)
        
        # plotting the pockets
        # Note that for the current iteration, it makes more sense not to draw the pockets, since they are interpreted as circles with
        # center points well off the table . . . it ends up looking more confusing if they are drawn.
        #for counter in range (0, len(pocket_list)):
        #    x = pocket_list[counter][0]
        #    y = pocket_list[counter][1]
        #    pocket_patch = plt.Circle((x, y), radius = .5, fc='g')
        #    self.ax.add_patch(pocket_patch)
        
        # making the actual animation. it is saved with a variable in case I want to save a video
        # in the future, so for now I am getting the warning that this pointer is not used.
        ani = animation.FuncAnimation(fig, self.animate,interval=int(1000/self.frame_rate), blit=True, init_func=self.animation_init, 
                                      frames=num_frames)
        
        # finally, show the animation
        plt.show()
        
        # some options for saving. Note that these require additional packages in python.
        #ani.save('animation.mp4', fps=60, bitrate=1000, extra_args=['-vcodec', 'libx264'])
        #ani.save('animation.mp4', fps=60, extra_args=['-vcodec', 'libx264'])
        #ani.save('animation.mp4')
    
    """this method will initialize the animation. It basically returns all the objects that need to move throughout the
    animation in their starting locations. In this case, it is just the balls. """
    def animation_init(self):
        for ball_patch in self.printable_balls:
            self.ax.add_patch(ball_patch)
        return self.printable_balls

    """perform one animation step- this function will return all of the patches that need to be plotted on the ith frame. The 
    current iteration just uses the closest timestep to the ith frame. In future iterations, I would like to use interpolation 
    to be more precise. at 30 frames per second, this is not noticeable. Also for future iterations, this function needs a revamp
    for efficiency's sake. See comments throughout."""
    def animate(self,i):
        patches_to_remove = []
        patches_to_return = []
        if i < 30:
            # create a delay in the animation.
            for counter in range(0,len(self.printable_balls)):
                ball = self.ball_list[counter]
                patch = self.printable_balls[counter]
                first_x = ball.position_x_record[0]
                first_y = ball.position_y_record[0]
                patch.center = (first_x, first_y)
        else:
            i = i-30
            # currently trusting that each entry in printable balls lines up with the corresponding entry in ball list.
            # this is a reasonable assumption, since they were added sequentially.
            for counter in range(0,len(self.printable_balls)):
                ball = self.ball_list[counter]
                patch = self.printable_balls[counter]
                
                # find closest timestep Current algorithm is horribly inefficient.
                # a binary search, or at least stop once the times start decreasing, is 
                # probably worth my while in the future. Also, once a ball stops moving,
                # we should be able to just use its last spot rather than iterate the lists.
                current_time = i*(1./self.frame_rate)
                closest_timestep = 0
                time_from_perfect = math.fabs(ball.time_record[0] - current_time)
                for timesteps in range(0, len(ball.time_record)):
                    check_time_from_perfect = math.fabs(ball.time_record[timesteps] - current_time)
                    if check_time_from_perfect <= time_from_perfect: # select the LAST timestep- in case multiple are the same.
                        # this becomes important for the final timestep, when the ball goes into a pocket.
                        time_from_perfect = check_time_from_perfect
                        closest_timestep = timesteps
                new_x = ball.position_x_record[closest_timestep]
                new_y = ball.position_y_record[closest_timestep]
                if new_x == None or new_y == None:
                    patches_to_remove.append(self.printable_balls[counter])
                else:
                    patch.center = (new_x, new_y)
            
            # assembling the return list, without any that have been sunk. The real reason for this is that
            # balls that have been sunk can't be removed from the list, or the animation fails to play multiple times.
        for counter in range(0, len(self.printable_balls)):
            patches_to_return.append(self.printable_balls[counter])
        for counter in range(0, len(patches_to_remove)):
            patches_to_return.remove(patches_to_remove[counter])
        
        return patches_to_return
    
    """calculating the appropriate max/min display. I am assuming that no balls are outside of the border to start with. if 
    they are, things will not work correctly (they won't be able to get inside), and they may not be displayed. This method
    returns the left, right, top, and bottom coordinates for the animation. """    
    def calculate_table_size(self):
        # start by picking the first wall for all the sides- we need something to compare to.
        left = self.wall_list[0][0]
        right = self.wall_list[0][0]
        top = self.wall_list[0][1]
        bottom = self.wall_list[0][1]
        # find the extremes- if anything is further out than the first side, it replaces this entry.
        for counter in range(0, len(self.wall_list)):
            x = self.wall_list[counter][0]
            y = self.wall_list[counter][1]
            if x > right:
                right = x
            if x < left:
                left = x
            if y > top:
                top = y
            if y < bottom:
                bottom = y
                
        # expanding borders slightly, so the lines arn't on the border of the viewing area.
        width_cushioning = math.fabs(left - right) * .1 # arbitrarily 10 percent
        height_cushioning = math.fabs(top - bottom) * .1 # arbitrarily 10 percent
        top += height_cushioning
        bottom -= height_cushioning
        left -= width_cushioning
        right += width_cushioning
        return [[left, right],[top, bottom]]

    """This function returns the amount of time it takes for the last ball to stop moving- ie, the last entry in the time_record for
    the ball that is moving longest. """
    def max_time(self):
        duration = 0
        for ball in self.ball_list:
            end = len(ball.time_record) - 1
            current_ball_duration = ball.time_record[end]
            if current_ball_duration > duration:
                duration = current_ball_duration
        return duration
    
    