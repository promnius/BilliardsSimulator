
# known issues: method take_shot does not handle case where cue ball does not exist or where one of the balls does
# not have an empty state history. see take_shot for more information

import Pool_Ball_Class
import math
import Impact_Solver_Class
import Simple_Visualization_Class
import My_ODE_Solver
import Complex_Animation_Class


"""An object representing a pool table. This object stores a list of balls, as well as wall and pocket locations, and includes the
base methods for moving balls around on the table and setting up their positions, although the algorithems for calculating new positions
are implemented by other classes."""
class Pool_Table():
    def __init__(self, game_type):
        self.setup_table(game_type)
        # creating all the objects that are needed (helper objects)
        # pens are for visualization of shots
        self.simple_pen = Simple_Visualization_Class.Plot_Drawing()
        self.complex_pen = Complex_Animation_Class.Complex_Animation()
        # see my_ODE_Solver.py to understand why a custom ODE solver was implemented
        self.smart_guy = My_ODE_Solver.ODE_Solver()
        self.crash = Impact_Solver_Class.Impact_Solver(self.list_all_balls, self.list_walls, self.list_pockets)

    """This method creates all the walls and pockets for the table. In pool, there are multiple legal table sizes available,
    but one was picked for the purpose of this simulation. All measurements are in meters. This method is used by all the game
    setup functions, since they all share the same table dimensions. """
    def create_walls(self):
        # creating the walls. for a single table, it was easiest to simply manually add each additional
        # point on the table. For future iterations, a more code-efficient technique should be developed.
        # 0,0 is bottom center. (or top center if table is rotated 180 degrees).
        pocket_depth = .1
        self.list_walls = []
        self.list_walls.append([-.604178,0])
        self.list_walls.append([.604178,0])
        x = .604178 + (pocket_depth * math.sqrt(2)) / 2
        y = - (pocket_depth * math.sqrt(2)) / 2
        self.list_walls.append([x, y])
        self.list_walls.append([x + .05715 * math.sqrt(2), y + .05715 * math.sqrt(2)])
        self.list_walls.append([.685, .0808])
        self.list_walls.append([.685, 1.313])
        self.list_walls.append([.685 + pocket_depth, 1.313])
        self.list_walls.append([.685 + pocket_depth, 1.4272])
        self.list_walls.append([.685, 1.4272])
        self.list_walls.append([.685, 2.66])
        x = .685 + (pocket_depth * math.sqrt(2)) / 2
        y = 2.66 + (pocket_depth * math.sqrt(2)) / 2
        self.list_walls.append([x, y])
        self.list_walls.append([x - .05715 * math.sqrt(2), y + .05715 * math.sqrt(2)])
        self.list_walls.append([.604178, 2.74])
        self.list_walls.append([-.604178, 2.74])
        x = -.604178 - (pocket_depth * math.sqrt(2))/ 2
        y =  2.74 + (pocket_depth * math.sqrt(2))/2
        self.list_walls.append([x, y])
        self.list_walls.append([x - .05715 * math.sqrt(2), y - .05715 * math.sqrt(2)])
        self.list_walls.append([-.685, 2.66])
        self.list_walls.append([-.685, 1.4272])
        self.list_walls.append([-.685 - pocket_depth, 1.4272])
        self.list_walls.append([-.685 - pocket_depth, 1.313])
        self.list_walls.append([-.685, 1.313])
        self.list_walls.append([-.685, .0808])
        x = -.685 - (pocket_depth * math.sqrt(2))/ 2
        y = .0808 - (pocket_depth * math.sqrt(2))/ 2
        self.list_walls.append([x, y])
        self.list_walls.append([x + .05715 * math.sqrt(2), y - .05715 * math.sqrt(2)])
        
        # creating the pockets
        pocket_radius = .47
        self.list_pockets = []
        self.list_pockets.append([-.685 - (pocket_radius * math.sqrt(2)) / 2 , 0 - (pocket_radius * math.sqrt(2)) / 2])
        self.list_pockets.append([.685 + (pocket_radius * math.sqrt(2)) / 2 , 0 - (pocket_radius * math.sqrt(2)) / 2])
        self.list_pockets.append([.685 + (pocket_radius * math.sqrt(2)) / 2 , 2.74 + (pocket_radius * math.sqrt(2)) / 2])
        self.list_pockets.append([-.685 - (pocket_radius * math.sqrt(2)) / 2 , 2.74 + (pocket_radius * math.sqrt(2)) / 2])
        self.list_pockets.append([-.685 - pocket_radius - .05, 2.74/2])
        self.list_pockets.append([.685 + pocket_radius + .05, 2.74/2])

    """For very basic unit tests, this function sets up a table with only one ball on it. Useful for testing the laws of physics,
    the ODE solver, and the interaction between balls and pockets. The simulations are simple enough that they can be visualized
    well with the 'simple' visualization. """    
    def one_ball_setup(self):
        self.create_walls()
        self.list_all_balls = []
        self.list_active_balls = []
        position_x = 0 # positions are unimportant, as long as the ball is on the table. positions will be re-assigned when a
        # shot is taken anyway, since this is the cue ball.
        position_y = .2
        ball = Pool_Ball_Class.Pool_Balls(position_x, position_y, "CUE_BALL")
        self.list_all_balls.append(ball)
        for ball in self.list_all_balls:
            self.list_active_balls.append(ball)
            
    """For slightly more complex unit tests than the 'one_ball_setup,' this function sets up a table with three balls on it
    (where one is a cue ball). This is useful for testing break mechanics and the interactions between balls. """        
    def three_ball_setup(self):
        self.create_walls()
        self.list_all_balls = []
        self.list_active_balls = []
        
        position_x = 0 # dummy positions so that the balls are on the table and not touching. see below for exact ball placement.
        position_y = .2
        ball = Pool_Ball_Class.Pool_Balls(position_x, position_y, "CUE_BALL")
        self.list_all_balls.append(ball)
        for counter in range(0,2):
            position_x += .25
            ball = Pool_Ball_Class.Pool_Balls(position_x, position_y, "NOT_CUE_BALL")
            self.list_all_balls.append(ball)
        
        # placing balls. We know that the position records have length of exactly 1 because I just created the balls, and this is the 
        # definition for how they are created.
        self.list_all_balls[1].position_x_record[0] = .033
        self.list_all_balls[1].position_y_record[0] = 2
        self.list_all_balls[2].position_x_record[0] = -.033
        self.list_all_balls[2].position_y_record[0] = 2
                
        for ball in self.list_all_balls:
            self.list_active_balls.append(ball)
        
    """The main game setup for the purpose of this project, this function sets up the table with 10 balls (9 game balls and
    a cue ball), in the formation most commonly recognized by the name '9-ball'. """   
    def nine_ball_setup(self):
        self.create_walls()
        self.list_all_balls = []
        self.list_active_balls = []
                
        position_x = 0 # dummy positions so that the balls are on the table and not touching. see below for exact ball placement.
        position_y = .2
        for counter in range(0,9):
            position_x += .25 # dummy value- will be replaced
            ball = Pool_Ball_Class.Pool_Balls(position_x, position_y, "NOT_CUE_BALL")
            self.list_all_balls.append(ball)

        # jenky way of setting initial positions. These are the values for a tightly racked set of balls on the size table selected
        # for this simulation. To make this code more versatile, I would need to calculate appropriate positions based on the existing
        # wall locations. All measurements in meters. 0,0 is bottom center. (or top center if table is rotated 180 degrees).
        self.list_all_balls[0].position_x_record[0] = 0
        self.list_all_balls[0].position_y_record[0] = 1.98
        self.list_all_balls[1].position_x_record[0] = -.028829
        self.list_all_balls[1].position_y_record[0] = 2.029933
        self.list_all_balls[2].position_x_record[0] = .028829
        self.list_all_balls[2].position_y_record[0] = 2.029933
        self.list_all_balls[3].position_x_record[0] = -.057658
        self.list_all_balls[3].position_y_record[0] = 2.079866
        self.list_all_balls[4].position_x_record[0] = 0
        self.list_all_balls[4].position_y_record[0] = 2.079866
        self.list_all_balls[5].position_x_record[0] = .057658
        self.list_all_balls[5].position_y_record[0] = 2.079866
        self.list_all_balls[6].position_x_record[0] = -.028829
        self.list_all_balls[6].position_y_record[0] = 2.129799
        self.list_all_balls[7].position_x_record[0] = .028829
        self.list_all_balls[7].position_y_record[0] = 2.129799
        self.list_all_balls[8].position_x_record[0] = 0
        self.list_all_balls[8].position_y_record[0] = 2.179732
        
        # adding cue ball
        cue_ball = Pool_Ball_Class.Pool_Balls(0,.635, "CUE_BALL")
        self.list_all_balls.append(cue_ball)
        
        for ball in self.list_all_balls:
            self.list_active_balls.append(ball)
            
    """This method re-racks all the balls based on the given game type. Useful for the end of a game, or, more specifically
    for the purpose of this break simulator, it allows you to reset the game after a break without creating a new table object.
    Future iterations will include the option for 8-ball, snookers, and potentially a 'custom' game setup."""
    def setup_table(self, game_type):
        if game_type == "UNIT_TEST_1_BALL":
            self.one_ball_setup()
        elif game_type == "UNIT_TEST_3_BALLS":
            self.three_ball_setup()
        elif game_type == "9_BALL":
            self.nine_ball_setup()
        else:
            print "Game style not implemented yet. 9 ball will be used. Error Code: 3409283714"
            self.nine_ball_setup()
        
    """This method takes a position, velocity, and angle for the cue ball, and solves the differential equations to determine the
    final resting points of all the balls. Because the intention of this software is to model breaks, the cue ball is re-placed on the
    table before each shot, and as such, this method does not handle the error where the cue ball does not exist. further modifications
    are planned to enable handling a scratch, but for now this method only takes the break shot. It also fails to handle the case where
    balls have a non-empty state history (a trivial fix- empty the state history before computations!), but again not an issue because
    the table is always re-racked before a break, so none of the balls have previous shot histories."""
    def take_shot(self,velocity, angle, x_position = None):
        # algorithem overview:
        # check for errors (no cue balls, balls that still have shot records)
        # moves cue ball based off of input.
        # while at least one ball has non-zero velocity:
            # integrate ball positions until impace
            # handle impact

        # check for the presence of exactly one cue ball.
        cue_counter = 0
        for ball in self.list_active_balls:
            if ball.is_cue_ball == True:
                cue_counter += 1
                cue_ball = ball
        if not cue_counter == 1:
            print "Error! There is NOT exactly one cue ball. Simulation will not take a shot."
        else:
            if x_position == None:
                # User chose not to set position of cue ball. Calculate appropriate position under the assumption that the user wants
                # to hit the middle of the first ball.
                cue_ball.position_x_record[0] = -(1.98 - .635) / math.tan(math.radians(angle))
            else:    
                cue_ball.position_x_record[0] = x_position
            
            # current modeling decision- y location is fixed at the edge of the kitchen.
            cue_ball.position_y_record[0] = .635
            cue_ball.velocity_x_record[0] = math.cos(math.radians(angle)) * velocity
            cue_ball.velocity_y_record[0] = math.sin(math.radians(angle)) * velocity
            
            done = False
            while not done:
                done_yet = self.smart_guy.solve_till_impact(self.list_active_balls, self.list_walls, self.crash)
                if done_yet == "ALL_BALLS_STATIONARY":
                    done = True
                # in case the last round sunk any balls.
                self.remove_ball()
    

    """In the event that a ball has entered a pocket, the x and y positions will be set to None. This method removes
     them from the list of active balls so that future computations won't need to check them for impact. Note that they
     are left in the list_all_balls so that they will still be drawn on plots or animations."""
    def remove_ball(self):
        for ball in self.list_active_balls:
            end = len(ball.position_x_record) - 1
            if ball.position_x_record[end] == None or ball.position_y_record[end] == None:
                self.list_active_balls.remove(ball)           
        
    """Returns the numboer of non-cue balls remaining on the table. Useful for generating a figure of merit after
    a break."""
    def num_balls_remaining(self):
        # returns number of non- cue balls remaining on table
        return len(self.list_active_balls)

    
    """Create a visual representation of the table. parameter drawing_style will indicate whether to use a simple
    plot where each calculated timestep for each ball is plotted as a point, or complex, where a movie-like animation
    is used to demonstrate the trajectories of balls in real time. the first option is excellent for debugging (you can
    identify which points were actually calculated by the solver), and for small numbers of balls, but becomes difficult
    to interpret with larger numbers of balls, such as a full break."""
    def draw(self, drawing_style):
        if drawing_style == "SIMPLE":
            print "Drawing of simple animation requested."
            self.simple_pen.draw(self.list_all_balls, self.list_walls)
        elif drawing_style == "ADVANCED":
            print "Drawing of complex animation requested."
            self.complex_pen.draw(self.list_all_balls, self.list_walls, self.list_pockets, 1)
        else:
            print "Other Draw options not implemented yet. Simple method being used. error 135424512."
            self.simple_pen.draw(self.list_all_balls, self.list_walls)

