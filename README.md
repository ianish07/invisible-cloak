# Invisible-Cloak

Python code using OpenCV to create an Invisibility Cloak just like the one in Harry Potter.
Here I have defined the cloak's color to be red, but you can go with any color. You just have to alter the Hue value to your fav color.

# How it works
The technique used is opposite to what Green Screening is. In green screening, we remove background but here we will remove the foreground frame.

Basic Algorithm:

1. Capture and store the background frame
2. Detect the defined color using color detection and segmentation algorithm.
3. Segment out the defined colored part by generating a mask.
4. Generate the final augmented output to create a magical effect.
