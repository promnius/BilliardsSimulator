import Table_Class
import matplotlib.pyplot as plt # for plotting final results. Not needed in current iteration- plots made in MATLAB.



"""similar functionality to a linspace for lists, this function returns a list with leng entries evenly spaced
between low and up."""
def lin_fill(low,up,leng):
    lin_list = []
    step = (up - low) / float(leng)
    for counter in range(leng):
        lin_list.append(low)
        low = low + step
    return lin_list

"""This function sweeps a grid of starting velocities and starting angles, calculates a break from each velocity/angle combo,
determines how many balls were sunk, and produces the data for creating a visual plot of this information. Note that the code 
for creating the visual was created in MATLAB, and not included here. This was used to answer the original question of the project:
what is the best break angle. While the data was fairly numerically unstable, trends were noticed for a slightly of center break having
the best chance of sinking at least one ball. Although this is consistent with some techniques suggested online, the numerical instability
combined with the modeling decision to ignore spin makes me feel that the results were inconclusive. """
def main():
    # some of the options for heatmap density/range.

    sweep_angles = lin_fill(85,91,6)
    sweep_velocities = lin_fill(16,24,4)

    #sweep_angles = lin_fill(65,90.5, 51)
    #sweep_velocities = lin_fill(12,26.5,29)
    
    print "sweep angles: " + str(sweep_angles)
    print "sweep velocities: " + str(sweep_velocities)
    
    num_balls_sunk = []
    inner_balls_sunk = []
    percentage_counter = 0 # for providing the user with percentage updates about progress.
    for angle in sweep_angles:
        #print "Angle: " + str(angle)
        percentage = (percentage_counter / float(len(sweep_angles))) * 100
        percentage_counter += 1
        print "Percentage Complete: " + str(percentage)
        for velocity in sweep_velocities:
            # take a shot, figure out how many balls were sunk for the given angle, velocity.
            #print "Velocity: " + str(velocity)
            my_table = Table_Class.Pool_Table("9_BALL")
            initial_ball_count = my_table.num_balls_remaining()
            my_table.take_shot(velocity, angle)
            #my_table.draw("ADVANCED")
            final_ball_count = my_table.num_balls_remaining()
            inner_balls_sunk.append(initial_ball_count - final_ball_count)
        num_balls_sunk.append(inner_balls_sunk)
        inner_balls_sunk = []
    
    # main graphics created using MATLAB, output not easily readable!
    print("Number of balls sunk for each angle,velocity combo:")
    print str(num_balls_sunk)
    
    
if __name__ == "__main__":
    main()     


