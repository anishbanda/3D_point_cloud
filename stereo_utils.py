import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import re
"""All necessary imports."""

def load_image(image_path):
    
    image = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    """Load image in grayscale mode."""
    
    if image is None:
        raise FileNotFoundError(f"Error: Unable to open the image file {image_path}.")

    return image
# load_image

def resize_images(left_img, right_img):
    
    height = min(left_img.shape[0], right_img.shape[0])
    width = min(left_img.shape[1], right_img.shape[1])
    left_resized = cv.resize(left_img, (width, height))
    right_resized = cv.resize(right_img, (width, height))
    """Resize both images to the same dimensions."""
    
    return left_resized, right_resized
# resize_images

def compute_disparity_map_sgbm(left_img, right_img, num_disparities, block_size):
    
    stereo = cv.StereoSGBM_create(minDisparity = 16,
                                   numDisparities = 512, # Adjust as needed (Must be divisible by 16)
                                   blockSize = block_size, # Adjust as needed
                                   P1 = 8 * 3 * block_size**2,
                                   P2 = 32 * 3 * block_size**2,
                                   disp12MaxDiff = 1,
                                   uniquenessRatio = 15,
                                   speckleWindowSize = 0,
                                   speckleRange = 2,
                                   preFilterCap=63,
                                   mode=cv.STEREO_SGBM_MODE_SGBM_3WAY)
    """Compute disparity map using StereoSGBM."""
    
    disparity_map = stereo.compute(left_img, right_img).astype(np.float32) / 16.0
    
    return disparity_map
# compute_disparity_map_sgbm

def compute_depth_map(disparity_map, baseline, doffs, focal_length):
    
    disparity_float = disparity_map.astype(np.float32)
    disparity_float[disparity_float <= 0] = 0.1 # Avoids division by 0
    depth_map = (focal_length * baseline) / (disparity_float + doffs)
    """Compute depth map using disparity map, baseline, focal length, and disparity offsets."""
    
    return depth_map
# compute_depth_map

def display_images(left_img, right_img, disparity_map, depth_map, title_left = "Left Image", title_right = "Right Image"):
    
    fig, axs = plt.subplots(1, 5, figsize = (20, 5))
    
    axs[0].imshow(left_img, cmap = 'gray')
    axs[0].set_title(title_left)
    axs[0].axis('off')
    """Display Left Image."""
    
    axs[1].imshow(right_img, cmap = 'gray')
    axs[1].set_title(title_right)
    axs[1].axis('off')
    """Display Right Image."""
    
    axs[2].imshow(disparity_map, cmap = 'gray')
    axs[2].set_title('Disparity Map')
    axs[2].axis('off')
    """Display Disparity Map."""
        
    axs[3].imshow(depth_map, cmap = 'plasma')
    axs[3].set_title('Depth Map')
    axs[3].axis('off')
    """Display Depth Map."""
    
    axs[4].imshow(disparity_map, cmap = 'plasma')
    axs[4].set_title('Disparity Map 2')
    axs[4].axis('off')
    """Display Plasma Disparity Map."""
    
    plt.show()
# display_images

def load_pfm(file_path):
    
    with open(file_path, 'rb') as f:
        
        header = f.readline().decode('latin-1').rstrip()
        color = header == 'PF'
        dim_match = re.match(r'^(\d+)\s(\d+)\s$', f.readline().decode('latin-1'))
       
        if dim_match:
            width, height = map(int, dim_match.groups())
        else:
            raise Exception('Malformed PFM header.')
        
        scale = float(f.readline().decode('latin-1').rstrip())
        
        if scale < 0:
            data_type = '<f'
        else:
            data_type = '>f'
        
        data = np.fromfile(f, data_type)
        data = np.reshape(data, (height, width, 3) if color else (height, width))
        data = np.flipud(data)
        """Loads .pfm file (Portable Float Map)."""
        
        return data, scale
# load_pfm

def parse_calibration_file(calib_file_path):
    
    with open(calib_file_path, 'r') as f:
        
        lines = f.readlines()
    """Parse calib.txt file."""
    
    # cam0 = [fx 0 cx; 0 fy cy; 0 0 1]
    cam_params = lines[0].split('=')[1].replace('[', '').replace(']', '').split(';')
    fx, fy = float(cam_params[0].split()[0]), float(cam_params[1].split()[1]) # Focal lengths
    cx, cy = float(cam_params[0].split()[2]), float(cam_params[1].split()[2]) # Principal points
    """Extracting cam0 values."""
    
    baseline = float(lines[3].split('=')[1])
    """Extarct baseline."""
    
    doffs = float(lines[2].split('=')[1])
    """Extract disparity offset."""
    
    return fx, fy, cx, cy, baseline, doffs
# parse_calibration_file

def compute_point_cloud(disparity_map, left_img, fx, baseline, cx, cy, doffs):
    
    height, width = disparity_map.shape
    points = []
    colors = []
    """Initialize point and color cloud data array."""
    
    if len(left_img.shape) == 2:
        left_img = cv.cvtColor(left_img, cv.COLOR_GRAY2RGB)
        
    valid_disparity_mask = disparity_map > 0.001  # Set minimum disparity threshold
    depth_map = np.zeros_like(disparity_map)
    depth_map[valid_disparity_mask] = np.clip((fx * baseline) / (disparity_map[valid_disparity_mask] + doffs), 0, 10000)
    """Avoids division by zero."""
    
    for y in range(height):
        for x in range(width):
            d = disparity_map[y, x]
            if d > 0.001: #Ensures valid disparity
                z = depth_map[y, x]
                X = (x - cx) * z / fx
                Y = (y - cy) * z / fx
                Z = z
                points.append([X, Y, Z])
                colors.append(left_img[y, x] / 255.0) # Add color from left image
    """Compute 3D coordinates for each valid pixel."""
    
    points = np.array(points)
    colors = np.array(colors)
    
    return points, colors
# compute_point_cloud