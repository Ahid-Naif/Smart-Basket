from huskylib import HuskyLensLibrary
import json
from time import sleep
from escpos import *

# Create the Mask Detection Robot class with the required settings:
class Object_Tracking_Robot:
    def __init__(self):
        # Define HusklyLens settings
        self.husky_lens = HuskyLensLibrary("I2C", "", address=0x32)
        self.cx = 160 # screen x venter
        self.cy = 120 # screen y center
        
        self.Tw = 130 # target width - this dimension determines how close to the camera the object should be 
        self.Ow = 0 # Object width
        self.Oh = 0 # Object height
        self.Ox = 0 # Object x center
        self.Oy = 0 # Object y center

        self.rightMotorSpeed = 0
        self.leftMotorSpeed = 0

        # Test the communication with the HuskyLens.
        print("First request testing: {}".format(self.husky_lens.knock()))
    
    # Decode the data generated by the HuskyLens.
    def decodeHuskyLens(self, obj):
        count=1
        if(type(obj)==list):
            for i in obj:
                # print("\t " + ("BLOCK_" if i.type=="BLOCK" else "ARROW_") + str(count) + " : " + json.dumps(i.__dict__))
                self.Ox = json.loads(json.dumps(i.__dict__))["x"]
                self.Oy = json.loads(json.dumps(i.__dict__))["y"]
                self.Ow = json.loads(json.dumps(i.__dict__))["width"]
                count+=1
        else:
            # print("\t " + ("BLOCK_" if obj.type=="BLOCK" else "ARROW_") + str(count) + " : " + json.dumps(obj.__dict__))
            self.Ox = json.loads(json.dumps(obj.__dict__))["x"]
            self.Oy = json.loads(json.dumps(obj.__dict__))["y"]
            self.Ow = json.loads(json.dumps(obj.__dict__))["width"]
            
    def OBJECT_TRACKING(self):
        # Get the recently read block from the HuskyLens
        self.decodeHuskyLens(self.husky_lens.blocks())
        vx = self.Ox - self.cx
        vy = self.cy - self.Oy + (self.Tw - self.Ow)
        # mapping
        self.rightMotorSpeed = vy - vx
        self.leftMotorSpeed = vy + vx
        self.MOVE_ROBOT()

    def MOVE_ROBOT(self):
        if self.rightMotorSpeed > 0:
            print("rightMotor - forward, Speed: {}".format(self.rightMotorSpeed))
        else:
            print("rightMotor - backward , Speed: {}".format(self.rightMotorSpeed))
        
        if self.leftMotorSpeed > 0:
            print("leftMotor - forward, Speed: {}".format(self.leftMotorSpeed))
        else:
            print("leftMotor - backward , Speed: {}".format(self.leftMotorSpeed))

# Define a new class object named 'robot':
robot = Object_Tracking_Robot()

while True:
    # Get blocks from the HuskyLens:
    robot.OBJECT_TRACKING()
    sleep(1)