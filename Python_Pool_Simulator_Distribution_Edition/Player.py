

import Table_Class

"""This function runs one simulation of a break at a given angle and velocity, then displays a visualization of the break. """
def main():
    # create pool table. Uncomment one line based on desired game format.
    #my_table = Table_Class.Pool_Table("UNIT_TEST_1_BALL")
    #my_table = Table_Class.Pool_Table("UNIT_TEST_3_BALLS")
    my_table = Table_Class.Pool_Table("9_BALL")
    #my_table = Table_Class.Pool_Table("asdf") # equivalent to playing 9-ball, except that a 'game doesn't exist' error will be thrown
        
    # make a break. choose an angle in degrees and an initial velocity in meters per second. format: my_table.take_shot(velocity, angle)
    # reasonable values for break speed are: 2-25
    # break speeds greater than this are unrealistic for a human (with speeds much greater than this having long computational times), 
    # negative break speeds are interpreted as shooting the other direction.
    # reasonable values for initial angle are: 65-115
    # angles outside of this range may result in the cue ball not starting on the table, since starting position is calculated based on angle
    # (operating under the assumption that the best break involves a direct hit on the center ball.) see Table_Class method 'take_shot' for 
    # options to set ball position manually.
    # (22.5, 84.5) is one example of a break angle that sinks 3 balls. Note that even a slight change in either angle or velocity will eliminate this result.
    my_table.take_shot(22.5, 84.5)
    
    # display this break for the user. options are simple and advanced.
    # simple may throw a runtime warning. It has to do with the matplotlib package not liking the number of points. it may be ignored.
    my_table.draw("SIMPLE")
    my_table.draw("ADVANCED")

if __name__ == "__main__":
    main()