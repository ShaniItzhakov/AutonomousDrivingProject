# Autonomous Driving Project

### The project
We developed a control algorithm that include video analysis capability to enable autonomous driving to avoid obstacles in a forest.

Using the algorithm, the car is able to estimate the depth of the objects and choose between left or right in case there is a close object.

### Analysis and deep learning
The object detecton is done using YOLOv5 with a ready weights file called 'best.pt' <br /><br />
<img width="281" alt="tree" src="https://user-images.githubusercontent.com/73496090/178832664-6909c718-359c-456f-a85b-b3342057a2af.png"><br />

The object's estimated distanse is given by the depth frame from the bag file.

In case the object is at a distance of 2.5 meters to 5 meters we will see a 45 degrees arrow, and in case the distance is less than 2.5 meters we will see a sharp arrow.<br />
Click ['example_video.mp4'](https://github.com/ShaniItzhakov/AutonomousDrivingProject/blob/main/example_video.mp4) for visualiation.

<img width="549" alt="pic2" src="https://user-images.githubusercontent.com/73496090/178831447-d546c5d9-0a9a-425d-b1a0-951279fccebd.PNG">

<img width="550" alt="pic" src="https://user-images.githubusercontent.com/73496090/178831506-c72bd482-e3eb-45e3-9c61-e140c3b05e88.PNG">

### Data collection
We used a RealSence stereo camera for the video capture and depth capture.
We used Python and Google Colaboratory Notebook as a platform to run the code.

### Running instructions
1. Upload the `best.pt` and the bag file that you have to the main folder in your drive. (you can use dose in the Videos.zip)
2. Open the `AutonomousDrivingProject.ipynb` in Google Colab
3. Rename the file name in the first row - `bagfile_name = '20220609_143137.bag' `
4. Run the `AutonomousDrivingProject.ipynb`

