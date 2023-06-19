<div id="top"></div>

<h1 align="center">:cat: The Pet Cat Bot </h1>

<div align="center">
    <img src="carpic148.jpg" alt="Logo" width="500" height=500">
</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="ucsdLogo.png" alt="Logo" width="200" height="50">
<h3>Team 8 | UCSD ECE / MAE 148: Autonomous Vehicle | Final Project</h3>
<p>
Spring 2023
</p>
</div>

- Mekhi Ellington (ECE)
- Mikhail Rossoshanskiy (ECE)
- Dehao Lin (MAE)
- Sankalp Kaushik (MAE)

![alt text](teampic148.jpg)


## Project Overview
We are building a laser-guided GPS mapper robot that functions as a cat.

## :octocat: Key Features
Our robot has two main features:

    1. Interactive control with laser;

    2. Collecting the route data.

That means we can guide the robot with a laser pointer, just like how we play with cats. The robot automatically collects location data while operating, and will save the location data for mapping around the area. 

PICTURE/VIDEO HERE 

## What have we done?
To achieve these two features, we focused our work on our VESC module, GNSS module, and OAKD Lite Camera module.

### VESC module - PyVESC
To implement movement and commands to the VESC. We ended up using the PyVESC Library. We were able to directly put values into the VESC script that would control the Servo and the Throttle control of the VESC. In PyVESC any value from 0.0 to 1.0 controls the steering of the servos with 0.0 making the wheels point all the way to the left. Meanwhile, 1.0 would point it to the right. It's the same thing with Throttle control, 0 being no movement and 1.0 being maxed throttle on the Motor. 
For implementation, we had to tweak certain parts of this. First, We found the speed of the VESC going from 0 to 1.0 is extremely fast. The first thing we did was set a threshold value on how fast it is capped at going even while at 100% throttle. We ended up using 0.35 as our threshold value. 
For the servo controls we started off using boundary boxes going from the left and the right of the camera's frame. With our 720x720 captured box from the camera. Initially, for the right, the values were set to less than 120 pixels of the frame would have the bot point directly left with a vESC value of 0.0, while servo point 0.35 would be less than pixel 180 and then 0.45 for less than 240. This is mirrored on the right side of the camera view but opposite. This resulted in very jerky servo movements at first but this ended up not working in the long run.
We ended up just switching to completely Analog steering. Instead, we just set the current pixel a laser is seen on and put it over 720 (720x720 pixel capture window) This results in us getting literally 720 points that we can accurately turn to after implementation. 

### GNSS module - 
location errors and data parsing 

### OAKD Lite Camera module - 
color detection and computer vision

## Contact

* Mekhi Ellington - mellingt@ucsd.edu
* Mikhail Rossoshanskiy - mrossosh@ucsd.edu
* Dehao Lin - delin@ucsd.edu
* Sankalp Kaushik - sskaushi@ucsd.edu

## Final Project Documentation

* [Final Project Presentation](https://docs.google.com/presentation/d/1CmsSRDc4tJDKef6RWzisFBF3TMSWqy2-ThQkxXycnEY/edit?usp=sharing)



