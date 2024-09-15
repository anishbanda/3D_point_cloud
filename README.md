# **Stereo Vision 3D Point Cloud Generation**

Read the instructions below to download the `2021 mobile dataset` from the Middlebury Stereo Vision dataset available at the link below:
[Middlebury Stereo Vision Dataset] (https://vision.middlebury.edu/stereo/data/)

## **Instructions for downloading dataset**
1. Click on the link above to access the Middlebury Stereo Vision Dataset
2. Scroll down to the [2021 mobile dataset] (https://vision.middlebury.edu/stereo/data/scenes2021/)
3. At the bottom of the page, you will find a download link for a `.zip` file containing the full dataset. 
4. Move the extracted `data` folder to the same directory where `main.py` and `stereo_utils.py` are located.

The program **REQUIRES** the `data` folder to be in the **SAME** directory as the `main.py` and the `stereo_utils.py` files to run properly

### Dataset Reference
D. Scharstein, H. Hirschmüller, Y. Kitajima, G. Krathwohl, N. Nesic, X. Wang, and P. Westling. [High-resolution stereo datasets with subpixel-accurate ground truth]. (https://www.cs.middlebury.edu/~schar/papers/datasets-gcpr2014.pdf`)
In German Conference on Pattern Recognition (GCPR 2014), Münster, Germany, September 2014.

## Pre-Requisites
Ensure the following are installed on your system.
1. Python (Any version 3.0 or better)
[Python] (https://www.python.org/downloads/)
2. OpenCV
```
pip install opencv-python
```
3. Open3D
```
pip install open3d
```
4. Matplotlib
```
pip install matplotlib
```
5. Numpy
```
pip install numpy
```

## Usage
After downloading the `data` folder and ensuring it is in the same folder as `main.py`, you can run the program by executing in any IDE:
```
python main.py
```
(Make sure you are in the right directory)

The program will then prompt you to enter the folder path like below:
```
Enter the folder path containing the stereo images and the calibration data (data/your_folder): 
```

### **Example Usage**
For this example I will use the `pendulum1` data set located in the `data` folder.
```
python main.py
Enter the folder path containing the stereo images and the calibration data (data/your_folder): data/pendulum1
Point cloud saved to data/pendulum1/output_point_cloud.ply
*3D Point Cloud will be displayed*
```

### _What's Actually Happening:_
The program will:
 - Load stereo images from the specified folder.
 - Compute the disparity map using OpenCV's StereoSGBM algorithm.
 - Generate 3D point cloud from the disparity map using camera calibration parameters provided within the specified folder.
 - Visualize the 3D point cloud using Open3D.

## Code Overview
`main.py`
1. Prompts user for for path to stereo image folder.
2. Loads the stereo images.
3. Calls functions from `stereo_utils.py`
  
`stereo_utils.py`
Contains the following utility functions:
`load_image`: Loads image in grayscale mode.
`resize_images`: Resize both images to same dimensions.
`compute_disparity_map `: Computes disparity map using StereoSGBM.
`parse_calibration_data`: Parse through `calib.txt` file to figure out calibration parameters.
`compute_point_cloud`: Compute 3D point cloud from disparity map.

________________________________________________________________________________________________________________________________________________________________________
