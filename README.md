# Loy-Eklundh Symmetry Detection

## About

A line of symmetry detector that finds a line of reflective symmetry in an image.
Created as a final project for the CS39R Symmetry and Topology seminar in Spring 2016.

It implements the algorithm from this Computer Vision research paper:
[Detecting Symmetry and Symmetric Constellations of Features](http://www.cse.psu.edu/~yul11/CourseFall2006_files/loy_eccv2006.pdf) by Loy and Eklundh.

## To Run

You need OpenCV, Matplotlib, and NumPy to run the script.

## How to Use
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

To save the image, run that same command but add a filename at the end to save the
line drawn version, like this:

`python3 detect.py butterfly.png 4.8 2.4 butterfly-symmetry.png`

## How it Works
How does the symmetry detection work? At a high level, essentially what 
is does is compare feature points on the image to those on the 
reflected version of the image. A feature point is essentially some sort
of distinctive point (really a small region around a point), like an edge,
corner, or something. These are found using the Scale Invariant Feature Transform (SIFT).

With each feature point comes its descriptor, which characterizes the region
right around that point. What this means is, if you were to have two different photographs of the same object and ran SIFT on each picture, ideally a keypoint at a certain spot on the object in image 1 should have a descriptor very similar to the descriptor on a point on the object in image 2 that corresponds to the same 'part' of the object.

In this case, our two images are the original and a flipped/mirrored version of it. Then, keypoints of original are matched with those of mirrored version based on how similar the descriptor is. The idea is that the mirrored keypoint is the reflected version from the original, that now looks like the original after reflection. Then, a weighted vote is cast for the line of symmetry that would create such a reflection.

The 'votes' are tallied and the result is the hexbin plot of (r, theta) values, which represent a line in polar coordinates.
