# About
This is code written to read in model information and render a scene using Whitted Ray Tracing. This code was initially written for Georgia Tech's CS3451 using Processing's Python scripting. I have since modified the project to run independent of the Processing environment.

# Running the code
To run, python 2.7 and all dependencies must be installed.
On the command line run 'python ray_tracer.py' to start the program. To load an image enter a number 0-9, and press enter. Input 'q' or any other key to quit the program.

# Scene information
The scenes are stored as .cli files. 

# Runtime and efficiency
As expected rendering each scene takes a significant amount of time. Potential optimizations (such as using numpy) will be explored soon.