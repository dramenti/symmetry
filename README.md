#Loy-Eklundh Symmetry Detection

##About

A line of symmetry detector that (sort of) implements the reflection detection from
this Computer Vision research paper:

[Detecting Symmetry and Symmetric Constellations of Features] (http://www.cse.psu.edu/~yul11/CourseFall2006_files/loy_eccv2006.pdf) by Loy and Eklundh.

##To Run

You need OpenCV, Matplotlib, and NumPy to run the script.

##How to Use
To run, first find an image you want to use it on, say 'butterfly.png' for example.

First, run `python3 detect.py butterfly.png` which will, using matplotlib, give you a
hexplot of (r, theta) values. The 'redder' the bin, the more 'votes' it has, meaning
it is more likely to be a line of reflection. Choose any red dot, and hover your cursor
over it to get the x and y coordinates. 'x' corresponds to r, and 'y' corresponds to theta.
Record these values somewhere. 

Then, run `python3 detect.py butterfly.png [r] [theta]` where
instead of [r] [theta] you put the numbers from the hexplot, e.g.
`python3 detect.py butterfly.png 4.8 2.4` which will display the image with a line drawn on it!

Then, press the **0** (ZERO) key to exit
(don't try to exit out of it normally, it doesn't work for some reason!)
