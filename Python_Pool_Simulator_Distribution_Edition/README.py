"""
Author: Kyle Mayer
Project Date: November, 2013
Language: Python 2.7 (some optional plotting code in MATLAB, not included in project files)
Dependencies: matplotlib
Main file for quick project overview: Player.py
"""

"""Project Purpose: to model a pool game break (9 ball specifically), to determine optimum break angles. Project conclusion: due to the 
numerical instability of a pool break, and the modeling decision to ignore spin, results are inconclusive, although a few trends were noted
that coincide with predictions from other sources. since the code is designed using a robust, recursively refined ODE solver, updating the 
physics model would be trivial from a coding perspective, though it is still quite difficult to accurately model all important effects."""

"""KNOWN MAJOR BUGS: The matplotlib package used for plotting animations does not play nicely with window resizes. resizing the window
during an animation will cause 'ghosts' of all the balls to be blitted on the screen if Blit is set to True. this error has been documented online, and the only
known solution is to redraw the entire screen between frames, which is resource intensive and unnecessary for all times except screen 
resize. future solutions: implement a different package for animations. 
Minor bugs are documented within their respective files, but do not effect the code for the purpose of this project, and are more like
suggestions for future features to make the code more useful in other scenarios."""

"""about the solver: rather than implementing ray intersection, an ODE solver was used for this simulation. Because of the number of
events caused by impacts between balls, and the relative simplicity of the differential equations (first order with no spin), a custom
ODE solver was developed that can dynamically determine step size and recursively refine step size around impact times to arbitrary precion.
This custom solver also handles impacts as part of the solver, reducing the coding complexity of handling events.
One reason for this decision was to make the code robust enough to handle effects like spin in the future, which will break models such as
ray intersection or stiff spring lattices.

Functionality was included to loop through many iterations of break angles and velocities, but the visualization is sub-par. the simulation
for a single break is fully implemented and easy to visualize."""

"""Player.py creates a table, takes a shot, and displays this shot for the user. It is the best script for getting a 
visual representation of what this project does.
Heatmap_Iterator.py is the other option, and will cycle through many breaks with no visual representation. """