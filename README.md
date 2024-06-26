# Readme

This open-source code allows one to compute zigzag persistence from a sequence of images (or a white and black video). The program outputs the corresponding barcodes for dimensions 0 and 1. This repository contains a Jupyter notebook and also a GUI.

![](https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/video_readme.gif)

## Requirements

The sofware needs the packages ```opencv-python```, ```dionysus```, ```numpy```, ```natsort```, ```Pillow``` and ```matplotlib```.
To run the experiments and compare the results, ```pandas``` is also required.

The program has been tested on Linux (Ubuntu 22.04 and Ubuntu 20.04). Note that is difficult to build/install Dionysus on Windows.

## Installation and Execution from sources

#### Option 1 (recommended): Using Anaconda.

The following instructions install the software using Anaconda. 
They have been tested on fresh installations of Ubuntu 22.04 and Ubuntu 20.04 in two different computers.

Anaconda is required, so if you do not have it in your system, install it following the instructions in the official website (https://docs.anaconda.com/free/anaconda/install/linux/).

Then, the following commands will clone the repository, create a fresh Conda environment, install the requirements and execute the GUI.

```
sudo apt-get install git cmake build-essential libboost-all-dev
conda create -n ZigZag python=3.10 pip
conda activate ZigZag
git clone https://github.com/jodivaso/ImageZigZag.git
cd ImageZigZag
pip install -r requirements.txt
python3 main.py
```

#### Option 2: Using Python and virtualenv.

The following instructions install and execute the software. They have been tested on a fresh installation of Ubuntu 22.04.

```
sudo apt-get install git cmake build-essential libboost-all-dev
sudo apt-get install python3-tk python3-pip
sudo apt-get install python3.10-venv
git clone https://github.com/jodivaso/ImageZigZag.git
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
python3 -m venv zigzag
source zigzag/bin/activate
cd ImageZigZag
python3 -m pip install -r requirements.txt
python3 main.py
```


## Example

The following images are part of the repository (examples folder):

<p align="center">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/3circles-3.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/3circles-2.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/3circles-1.jpg" width="150">
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
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/3circles-barcode.png">

</p>


## Description of the software

This software implements the algorithms described in the paper *Zigzag persistence for image processing: new software and applications*.
The involved algorithms Algorithms have been implemented as Python functions using OpenCV and Numpy to read the images, 
the library [Dionysus 2](https://mrzv.org/software/dionysus2/) for computing the zigzag modules and Matplotlib to draw the barcode.

First of all, we have implemented an algorithm to build a simplicial complex where the number of vertices,
edges and triangles in the complex is smaller than in the triangulation
of the cubical complex of a binary image and in the
Vietoris–Rips complex. This is done in a function called ```binaryImageToSimplicialComplex```. We consider a binary image *I* with {nrows} rows and \texttt{ncols} cols. For each white pixel at position *(i,j)*, the corresponding vertex in the simplicial complex is given by the formula *i x numCols + j*. 

As a second step, we have defined a function called ```imageListToZigzagFiltration``` that, from a list of binary images of the same size, constructs a simplicial complex and a zigzag filtration like the one required by the Dionysus 2 software. To use Dionysus 2, for each simplex in the complex we must specify a list of times when it enters and leaves the filtration. This information must be provided as a list of lists, ```times```. For the *i*-th simplex in the filtration, ```times[i]``` is a list of times, where values in even positions (counting from 0) specify when the simplex is added to the complex and odd positions when it is removed. 

Once the zigzag filtration has been constructed, we use the Dionysus 2 function called ```zigzag\_homology\_persistence``` to determine the zigzag barcode associated to the filtration. Since the Dionysus software only provides the generators of the cycles that are still alive in the right-most homology group in the sequence, we have modified the internal behavior of this function in order to obtain the generators of all bars. To this aim, a global variable named ```all_generators_list``` is defined, and the Dionysus function ```detail``` (an optional callback argument, which gets called back after every step of the zigzag) is modified by adding the cycles to the list at each step.  Finally, if the optional parameters ```interval-length```, ```generator-min-length```, and ```generator-max-length``` are introduced, we select the bars that satisfy the desired conditions and draw them using our new function ```plot_zigzag_bars```.

These algorithms are also implemented in a Jupyter notebook, available also in this repository.

To allow users to apply our programs in an easier way, we have also developed a graphical interface (the image above). The new software inputs a set of binary images and it allows the user to decide the order of the images (to compute the zigzag persistence).  
The user can choose the dimensions for which the barcode will be determined (0 or/and 1), the minimum length of a bar to be showed and the minimum and maximum number of simplices (vertices or edges) in a generator that are needed to be showed in the barcode. It is also possible to decide whether the interval generators are shown in the barcode. The result is a graphical representation of the barcode diagrams shown within the application.
 
## CASABee example

The following image is a processed frame of one of the sample videos provided by the CASABee software:

![](https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/frame_video_CASABee.jpg)

We can compute the zigzag barcode of the video, to track the 1-dimensional holes. All circles (which correspond to motile spermatozoa) 
are detected (except for the ones in the borders, since they are not complete circles). The following (default) parameters are used:
- ```interval-length``` is set to half of the number of frames (to detect circles that live at least in half of the video)
- ```generator-min-length``` is set to 1 (but any value will work), i.e., we do not need to remove minor holes (there are barely overlaps)
- ```generator-max-length``` is set to 0, so we do not need to limit the size (we are interested in all holes)

Note that 1-dimensional homology is necessary (the number of connected components is not the same as the number of holes).

![](https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/result_video_CASABee.jpg)



## Experiments

The folder ```Experiments``` includes:
- A folder named ```dataset``` with 20 binary videos of different objects moving around the space to perform the experiments.
- A csv file named ```ground_truth.txt``` which contains the real number of connected components (0-dimensonal homology) and holes (1-dimensional homology) that appears in at least 20 frames of each video.
- A Jupyter notebook entitled ```Experiments.ipynb```, which includes the code and explanations to reproduce the experiments and get the results.
- A folder ```output_dataset``` which contains:
    - The zigzag barcodes (in both dimensions 0 and 1) of each video
    - A CSV file ```results.csv``` that contains information about:
        - The required time to build the reduced simplicial complex with our method for each video
        - The required time to compute the zigzag persistence with our reduced simplicial complexes for each video
        - The required time to compute the cubical complexes for each video
        - The required time to compute the zigzag persistence using cubical complexes for each video
        - The required time to compute the Vietoris-Rips complexes for each video
        - Size of the different reduced simplicial complexes, cubical complexes and Vietoris-Rips
        - Connected components and holes tracked by the method



## Comparison with classic alternatives for tracking

A classical object tracking method (a baseline approach) usually consists of three steps:

1. Object detection, for example using the ```findContours``` method (from OpenCV) or
the Hough transform (for the specific case of circle detection).

3. Centroid tracking, i.e. computation the centroid of each object and centroid matching
in subsequent frames according to the Euclidean distance.

5. (Optional) Filtering of the results based on each object contour area, aspect ratio,
SIFT/SURF features, etc.

The main benefit of the zigzag method is that it allows to perform the three steps
automatically, i.e., it allows tracking objects in an automatic way (in the sense that the
method indicates in which frames each object appears and disappears). Compared to the
Hough transform, this method also allows one to track holes other than circles. This is
not important for some of our examples, where Hough transform with tracking based on
distances is enough, but for other types of videos (for example, those of objects with different
shapes in the repository) the Hough transform does not fit. See, for example, the following figure:

<p align="center">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example2/example_response1.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example2/example_response2.jpg" width="150">
</p>

This figure is a sequence of two binary digital images. Both the zigzag method and the Hough
transform permit detecting and tracking the circles (holes) correctly. Note that the circles
change their shape slightly from one frame to the next.

However, in the following sequence of two binary digital images Hough transform will not work since
the objects do not have a circular shape. Both the ```findContours``` method (combined with
tracking based on distances) and the zigzag will work.

<p align="center">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example3/example_response1.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example3/example_response2.jpg" width="150">
</p>


It is also worth noting that the shape of the objects (not just their positions) can usually
vary slightly over the different frames. The zigzag method can deal with these situations.
The baseline approach would use, as already mentioned, the ```findContours``` method and a
tracking based on distances with a filtering based on object area, but if the filtering is not
done (or it is performed but not properly) and/or the objects change more than expected,
then zigzag will detect them as different objects (as desired), but the classical method could
match them incorrectly.

<p align="center">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example1/example_response1.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example1/example_response2.jpg" width="150">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example1/example_response3.jpg" width="150">
</p>

In the previous sequence binary digital images the circles change their shape
in each frame. Hough transform will not work properly since one of the objects does not
have a circular shape in frame 2. The ```findContours``` method (combined with tracking based
on distance with no filtering) will not work, since one of the circles is transformed into a
square, but the ```findContours``` method would detect it as the same contour since it is the
closest one with a similar area (i.e., the left circle appearing in the first frame is related to
the square in the second frame). The zigzag method will detect 3 holes correctly, one living
during three frames.

<p align="center">
<img src="https://raw.githubusercontent.com/jodivaso/ImageZigZag/master/readme_imgs/examples_comparison/example1/example_response1_barcode.jpg">
</p>

Of course, for cases like this or other similar variants, the classical method will work if
a more sophisticated filtering is used, for instance based on SIFT/SURF features or other
techniques depending on the objects to detect.

The advantage is that the zigzag does the tracking of connected components and holes for free, 
but the main drawback is the running time: the new method is not competitive with classical techniques.

## Quantitative evaluation comparison

The previous experiments (file ```Experiments/Comparison.ipynb```) showed that the zigzag approach is able to detect about 96% of connected components and about 99% of holes of the input dataset.
To have further quantitative evaluation, we have performed comparisons using the following baseline approaches:

1) Baseline approach 1: Use of a detector and then tracking using OpenCV algorithms by means of the MultiTracker class.
2) Baseline approach 2: Use of a detector and then tracking using OpenCV algorithms without using the MultiTracker class.
3) Baseline approach 3: Use of a detector and tracking based on centroids distance.

OpenCV includes several tracking algorithms, such as CSRT, KCF, Boosting, MIL, MedianFlow and Mosse. Latest OpenCV is also compatible with other tracking algorithms, such as Nano and Vit, but this requires to download external models that are not included in OpenCV. We did not try such tracking algorithms.
The tracking algorithms must be initialized with the bounding box for the targets, i.e., we need a detector to find the bounding boxes in the first frame of the objects to be tracked. To do this, we employed two options: the Hough transform and the findContours method (also tuned to detect the inner contours to find the holes).

For the baseline approaches 1 and 2, we evaluate all combinations of detectors with each tracking algorithm, i.e., each video of the dataset is evaluated 18 times (3 detectors and 6 tracking algorithms). The third approach is also repeated using both the Hough transform and the findContours method (in this case, the tracking is performed with the classical centroids distance approach). In all three experiments, we consider an object to be correctly tracked if it has been detected in at least 20 consecutive frames (as in the zigzag experiments). 

The folder ```Experiments/output_comparison``` also contains the images of the tracking process for combination of baseline method, video, detector and tracking algorithm. The file ```Experiments/Comparison.ipynb``` allows one to replicate the whole comparison.



|       **Method**      | **findContours - Min H0** | **findContours - Mean H0** |     **findContours - Max H0**    |
|:---------------------:|:-------------------------:|:--------------------------:|:--------------------------------:|
| **Baseline method 1** |        93.19 (KCF)        |            97.28           |    98.95 (CSRT, Boosting, MIL)   |
| **Baseline method 2** |     93.72 (MedianFlow)    |            97.80           | 98.95 (CSRT, Boosting, KCF, Mil) |
| **Baseline method 3** |             -             |              -             |              0.9634              |

Table 1: Results of computing H0 using findContours and the three baseline methods. The numbers represents the percentage of connected components (100*detected/ground_truth) detected by the algorithms 
For baseline methods 1 and 2, we provide the min, mean and max values of the six tracking algorithms that have been tested in each case. Parentheses indicate the name of the tracking algorithm that achieved the min and max score.
Note that the third baseline method performs the tracking via centroid distance, thus no tracking algorithms are employed.



|       **Method**      | **Hough - Min H1** | **Hough - Mean H1** | **Hough - Max H1** | **findContours - Min H1** | **findContours - Mean H1** | **findContours - Max H1** |
|:---------------------:|:------------------:|:-------------------:|:------------------:|:-------------------------:|:--------------------------:|:-------------------------:|
| **Baseline method 1** |        65.69       |        74.31        |        76.47       |        67.64 (KCF)        |            92.15           | 99.01 (CSRT, Boosting, MIL) |
| **Baseline method 2** |        74.51       |        75.98        |        76.47       |        95.09 (KCF)        |            98.03           | 99.01 (CSRT, Boosting, MIL) |
| **Baseline method 3** |          -         |          -          |        77.45       |             -             |              -             |           96.56           |

Table 2: Results of computing H1 using Hough and findContours as detectors for the three baseline methods. The numbers represents the percentage of holes (100*detected/ground_truth) detected by the algorithms 
For baseline methods 1 and 2, we provide the min, mean and max values of the six tracking algorithms that have been tested in each case. Parentheses indicate the name of the tracking algorithm that achieved the min and max score.
Note that the third baseline method performs the tracking via centroid distance, thus no tracking algorithms are employed.

## A note on the computation time

Although the zigzag computation works for image and video processing, it is, as expected, much slower than any classical method. Indeed, it is well-known that current persistence-based algorithms applied to image processing are not competitive to non-persistence modern approaches. Indeed, computing usual persistent homology for datasets arising in real-world applications only became feasible in recent years due to optimizations that exploit various structural properties and algebraic identities of the problem (see this paper: [Efficient Computation of Image Persistence](https://arxiv.org/abs/2201.04170)). Thus, researchers and software developers of the main persistence software (Gudhi, Dionysus, Perseus, Ripser,...) are making great efforts to improve performance. 

To the best of our knowledge, this is the first library that allows one to analyze images and videos applying zigzag persistence, also offering a simple graphical interface. We hope this is a first step to extend the use of zigzag homology in image processing and we hope to incorporate the improvements that the community will surely achieve for zigzag computation (which is the current bottleneck).
