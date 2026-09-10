# Classical Computer Vision Concepts Archive

This repository contains all modules used when learning about computer vision in course material, translated to Python (except for 3D-2D projections)

## Project Overview

Archive is organized into distinct directories representing foundational computer vision tasks:
  1. Edge detection using kernels, filters, and operators
  2. Using the Circular and Linear Hough Transform to determine the longest line in an image, as well as circles in various sizes
  3. 3D to 2D projections, which uses matlab to implement camera projection models, coordinate transformations. Also includes utility functions for projecting 3D points to a 2D plane. 

## How to run scripts

1. git clone this repo: 

```
git clone https://github.com/abd-alaj/Classical-CV-Concepts
```

1. you will see the following folder structure: 

```
.
├── 3D_to_2D_projections_MATLAB
├── edge_detection_filters_and_operators
└── linear_circular_hough_transform
```

### MATLAB Based `.m` files

1. open the respective folder (with `.m`) in MATLAB or Octave, the code is compatible with both
2. run the following in the command console or terminal: 
  - **MATLAB:** `main` 
  - **Octave:** `run main.m`

### Python Based `.py` Files

1. change to the main github directory of the python module (or the root directory, but ensure the directory to `requirements.txt` is changed to the relative one in step 3.)
2. create a virtual environment in python: `python -m venv venv`

3. active the virtual environment: `source venv/bin/activate`

4. install the dependencies in the `requirements.txt` file: `pip install -r requirements.txt`

## Requirements 

- MATLAB or Octave
- Python (as of writing, the python version used is 3.8)

## To-do 

- rewrite the 3D to 2D coordinate projections in python, rather than MATLAB/Octave
