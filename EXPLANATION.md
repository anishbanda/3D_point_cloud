# **Reasoning for use of Semi-Global Block Matching**

I used the Semi-Global Block Matching (SGBM) method to compute the disparity map 
because it strikes a good balance between computational efficiency and accuracy 
for stereo vision tasks. Compared to simpler block matching algorithms, SGBM 
considers dependencies across a larger pixel neighborhood, allowing it to
reduce noise and provide a more accurate estimate for complex scenes.

# **Room for Improvement**

Despire using SGBM, the results of this task fall short of what I was aiming to
achieve. The generated 3D point cloud is not as accurate or complete as I hoped.
Key areas of the image in the middle are often missing or distorted when generated
as a 3D point cloud, and the output is far from a perfect 3D reconstruction. The 
program is also limited in functionality because it only works with the specific 
2021 mobile dataset from the Middlebury Stereo Vision dataset, which prevents 
applicability for real-world use cases.

# **Learning Points**

**Room for Algorithmic Improvement**
While SGBM remains effective for many cases, I learned that other method, such as
deep learning-based stereo matching algorithms, yield better results in more
diverse environments. If I were to redo the project I would definetely use a deep
learning approach hoping for a better result. This would also help with the
limitations my current program faces which is how its limited to only the dataset
and offets no real-world applicability.

**Limitations of 3D Reconstruction**
This project made me aware of how difficult it is to generate a perfect 3D 
reconstruction from stereo images. The output is heavily dependent on the quality 
of the disparity map. Even with the proper calibration data and a provided dataset,
the desired output was still unachievable for me. Testing out different methods to
achieve the same end result became exhausting and I reached a roadblock in a sense.

**Importance of Camera Calibration**
I learned how imperative camera calibration parameters such as focal length, 
baseline, and disparity offset are in producing accurate depth estimates. Even 
the smallest innacurracies in any one of those values can lead to a distortion 
in the generated 3D point cloud. This highlights the need for precise calibrations
in real-world applications.

**Challenges with Stereo Matching**
After implementing and experimenting with the SGBM algorithm, I learned how each
stereo image requires its own number of disparities and block sizes. For instance, 
areas of the scene with low texture or poor contrast between objects made it 
difficult for the algorithm to compute reliable disparities.
