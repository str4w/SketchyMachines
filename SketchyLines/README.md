# SketchyMachines: Sketchy lines
Sketchy Lines is a simple sketching approach which uses the Canny edge detector
on the image returned from the webcam.  The results vary - wildly - dependent
on the noise in the image.  The system accumulates lines from multiple images,
which puts emphasis on the lines that repeat, making them heavier.  Some 
randomness is introduced when it is vectorized, to avoid having jaggy lines fall
one on top of another precisely.
