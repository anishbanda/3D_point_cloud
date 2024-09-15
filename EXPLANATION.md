# **Reasoning for use of Semi-Global Block Matching**

I used the Semi-Global Block Matching (SGBM) method to compute the disparity map 
because it strikes a good balance between computational efficiency and accuracy 
for stereo vision tasks. Compared to simpler block matching algorithms, SGBM 
considers dependencies across a larger pixel neighborhood, allowing it to
reduce noise and provide a more accurate estimate for complex scenes.

# _Room for Improvement_

Despire using SGBM, the results of this task fall short of what I was aiming to
achieve. The generated 3D point cloud is not as accurate or complete as I hoped.
Key areas of the image in the middle are often missing or distorted when generated
as a 3D point cloud, and the output is far from a perfect 3D reconstruction. The 
program is also limited in functionality because it only works with the specific 
2021 mobile dataset from the Middlebury Stereo Vision dataset, which prevents 
applicability for real-world use cases.
