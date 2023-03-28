# Readme


## Installation and Execution from sources

Python (version 3.8 or higher) and ```pip``` must be installed previously.

The following commands clone the repository, install the requirements and execute the program.

```
git clone https://github.com/jodivaso/ImageZigZagPersistence.git
cd ImageZigZagPersistence
pip install -r requirements.txt
python3 main.py
```

## Example

The following images are part of the repository (examples folder):

<p align="center">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZagPersistence/master/examples/3circles-3.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZagPersistence/master/examples/3circles-2.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZagPersistence/master/examples/3circles-1.jpg" width="150">
</p>


In the first two images, three 1-dimensional classes
appear, whereas the last one only contains two. One of the holes
lives in the three images (top left corner; some pixels are different, but the hole is essentially the same); another 1-dimensional
class appears in the first image (top right) and disappears in
the third one; there is a hole that is only shown in the first image (bottom) and finally, another homology class appears in the
second image (bottom right corner) and is still alive in the third
image. We can obtain this information by computing the zigzag
barcode:

<p>
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZagPersistence/master/examples/3circles-barcode.png">

</p>

## CASABee example

The following image is a processed frame of one of the sample videos provided by the CASABee software:

![](https://raw.githubusercontent.com/jodivaso/ImageZigZagPersistence/master/examples/frame_video_CASABee.jpg)

We can compute the zigzag barcode of the video, to track the 1-dimensional holes. All circles (which correspond to motile spermatozoa) 
are detected (except for the ones in the borders, since they are not complete circles). The following (default) parameters are used:
- ```interval-length``` is set to half of the number of frames (to detect circles that live at least in half of the video)
- ```generator-min-length``` is set to 1 (but any value will work), i.e., we do not need to remove minor holes (there are barely overlaps)
- ```interval-length``` is set to 0, so we do not need to limit the size (we are interested in all holes)

Note that 1-dimensional homology is necessary (the number of connected components is not the same as the number of holes).

![](https://raw.githubusercontent.com/jodivaso/ImageZigZagPersistence/master/examples/result_video_CASABee.jpg)
