from stereo_utils import load_image, resize_images, compute_disparity_map_sgbm, parse_calibration_file, compute_point_cloud
# Import methods from stereo_utils.py
import os
import open3d as o3d
import cv2 as cv

def main():
    
    folder_path = input("Enter the folder path containing the stereo images and the calibration data (data/your_folder): ")
    # Prompts user for folder path
    
    left_image_path = os.path.join(folder_path, "im0.png")
    right_image_path = os.path.join(folder_path, "im1.png")
    calib_file_path = os.path.join(folder_path, "calib.txt")
    disparity_map = os.path.join(folder_path, "disp0.pfm")
    # Assigns necessary file paths
    
    fx, fy, cx, cy, baseline, doffs = parse_calibration_file(calib_file_path)
    # Parse calibration data
    
    left_img = load_image(left_image_path)
    right_img = load_image(right_image_path)
    # Load left and right images
    
    if left_img.shape != right_img.shape:
        left_img, right_img = resize_images(left_img, right_img)
    # Resize images if necesssary
    
    disparity_map_created = compute_disparity_map_sgbm(left_img, right_img, num_disparities=224, block_size=13)
    # Compute disparity map using StereoSGBM
    
    smoothed_disparity_map = cv.bilateralFilter(disparity_map_created, d=5, sigmaColor=25, sigmaSpace=25)
    # Smooths the disparity map
    
    
    points, colors = compute_point_cloud(smoothed_disparity_map, left_img, fx, baseline, cx, cy, doffs)
    # Compute point cloud
    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    # Create Open3D point cloud
    
    output_ply_file = os.path.join(folder_path, "output_point_cloud.ply")
    o3d.io.write_point_cloud(output_ply_file, pcd)
    print(f"Point cloud saved to {output_ply_file}")
    # Save point cloud to .ply file
    
    pcd = o3d.io.read_point_cloud(output_ply_file)
    o3d.visualization.draw_geometries([pcd])
    # Load and visualize point cloud
# main
    
if __name__ == "__main__":
    main()