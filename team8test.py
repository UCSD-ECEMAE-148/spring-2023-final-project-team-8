#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np
import time

#VESC class
class VESC:
    ''' 
    VESC Motor controler using pyvesc
    This is used for most electric scateboards.
    
    inputs: serial_port---- Serial device to use for communication (i.e. "COM3" or "/dev/tty.usbmodem0"
    has_sensor=False------- default value from pyvesc (Whether or not the bldc motor is using a hall effect sens)
    start_heartbeat=True----default value from pyvesc (Whether or not to automatically start the heartbeat thread that will keep commands
                                alive.)
    baudrate=115200--------- baudrate used for communication with VESC
    timeout=0.05-------------time it will try before giving up on establishing connection(timeout for the serial communication)
    
    percent=.2--------------max percentage of the dutycycle that the motor will be set to
    
    In Donkey framework all these parameters can be configured in the myconfig.py file
    outputs: none
    
    
    
    VESC class defines functions for controlling the steering(0-1) and throttle(as a percent of max allowed) 
    using the PyVesc library.
    
    Note that this depends on pyvesc, but using pip install pyvesc will create a pyvesc file that
    can only set the speed, but not set the servo angle. 
    
    Instead please use:
    pip install git+https://github.com/LiamBindle/PyVESC.git@master
    to install the pyvesc library
    '''
    def __init__(self, serial_port, percent=.2, has_sensor=False, start_heartbeat=True, baudrate=115200, timeout=0.05, steering_scale = 1.0, steering_offset = 0.0 ):
        
        try:
            import pyvesc
        except Exception as err:
            print("\n\n\n\n", err, "\n")
            print("please use the following command to import pyvesc so that you can also set")
            print("the servo position:")
            print("pip install git+https://github.com/LiamBindle/PyVESC.git@master")
            print("\n\n\n")
            time.sleep(1)
            raise
        
        assert percent <= 1 and percent >= -1,'\n\nOnly percentages are allowed for MAX_VESC_SPEED (we recommend a value of about .2) (negative values flip direction of motor)'
        self.steering_scale = steering_scale
        self.steering_offset = steering_offset
        self.percent = percent
        
        try:
            self.v = pyvesc.VESC(serial_port, has_sensor, start_heartbeat, baudrate, timeout)
        except Exception as err:
            print("\n\n\n\n", err)
            print("\n\n fix permission errors")
            time.sleep(1)
            raise
    ''' This particular file only shows the implementation involving the steering and throttle control from VESC
     `VESC.py of the PYVesc repository can be referred for additional functionalities''' 
        
    def run(self, angle, throttle):
        
        '''Input angle (0-1) and throttle (0 - 1)
            Steering center is at an angle of 0.5 for ECE/MAE 148. The offset can be adjusted using steering offset
            attribute'''
        
        self.v.set_servo((angle * self.steering_scale) + self.steering_offset)
        self.v.set_duty_cycle(throttle*self.percent)

# Create pipeline for CV
pipeline = dai.Pipeline()

# Define source and output
camRgb = pipeline.create(dai.node.ColorCamera)
xoutRgb = pipeline.create(dai.node.XLinkOut)

xoutRgb.setStreamName("rgb")

# Properties
camRgb.setPreviewSize(720, 720)
camRgb.setInterleaved(False)
camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.RGB)

# Linking
camRgb.preview.link(xoutRgb.input)

#Starting Vesc Module
VESC_module = VESC('/dev/ttyACM0')
# Connect to device and start pipeline
with dai.Device(pipeline, usb2Mode=True) as device:

    print('Connected cameras:', device.getConnectedCameraFeatures())
    # Print out usb speed
    print('Usb speed:', device.getUsbSpeed().name)
    # Bootloader version
    if device.getBootloaderVersion() is not None:
        print('Bootloader version:', device.getBootloaderVersion())
    # Device name
    print('Device name:', device.getDeviceName())

    # Output queue will be used to get the rgb frames from the output defined above
    qRgb = device.getOutputQueue(name="rgb", maxSize=4, blocking=False)
    
    while True:
        inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
    # Take each frame
        frame = inRgb.getCvFrame()
        
        hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

        lower_red = np.array([0,255,0])
        upper_red = np.array([255, 255, 255])
        mask = cv2.inRange(frame, lower_red, upper_red)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(mask)
        ##print(maxLoc[0],maxLoc[1])
	
        cv2.circle(frame, maxLoc, 20, (0, 0, 255), 2, cv2.LINE_AA)
       # cv2.imshow('Track Laser', frame)
        if((maxLoc[0] != 0) and (maxLoc[1] != 0)):
            if((maxLoc[0] > 240) and (maxLoc[0] < 480)):
                VESC_module.run(0.5,0)
            if(maxLoc[0] < 240):
                if(maxLoc[0] < 180):
                    if(maxLoc[0] < 120):
                        VESC_module.run(0,0)
                    VESC_module.run(0.35,0)
                VESC_module.run(0.45,0)
            
            if(maxLoc[0] > 480):
                if(maxLoc[0] > 540):
                    if(maxLoc[0] > 600):
                        VESC_module.run(1,0)
                    VESC_module.run(0.65,0)
                VESC_module.run(0.55,0)
            
        

        # Retrieve 'bgr' (opencv format) frame
        #cv2.imshow("rgb", inRgb.getCvFrame())

        if cv2.waitKey(1) == ord('q'):
            break
