# Autonomous Drone Project

### The project
We developed a control algorithm that include video analysis capability to enable autonomous drone to avoid obstacles in a forest.

The drone is able, using the algorithm, to dodge the obstables right and left that he encounters in the video and be aware of the depth between himself and the obstacles.

We visualised the movement of the drone, it's path and the distance from the drone to the obstacles in the video that we analyzed.

### Analysis and deep learning
The alalysis of the obstacles is used by deep learning that identifies by color of depth from the video analysis.
Then, we found using the identification the x and y parameters of each obstacle and by that we figured out how to calculate the path of the drone.

<img width="549" alt="pic2" src="https://user-images.githubusercontent.com/73496090/178831447-d546c5d9-0a9a-425d-b1a0-951279fccebd.PNG">

<img width="550" alt="pic" src="https://user-images.githubusercontent.com/73496090/178831506-c72bd482-e3eb-45e3-9c61-e140c3b05e88.PNG">

### Sources
We used a RealSence camera for the video capture and depth capture.
We used Python and Google Colaboratory Notebook as a platform to run the code.

### Running instructions
Google Colaboratory Notebook is required.

Run the following two commands in the terminal:
(you need to "cd" to your files folder and then run the "jupyter notebook targetfile.ipynb" command).

> - cd ~YourFilesFolder
> - jupyter notebook targetfile.ipynb

<img width="281" alt="tree" src="https://user-images.githubusercontent.com/73496090/178832664-6909c718-359c-456f-a85b-b3342057a2af.png">
