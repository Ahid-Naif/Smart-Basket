from huskylib import HuskyLensLibrary
import json
from time import sleep
from escpos import *
import RPi.GPIO as GPIO          
import sys

minSpeed = 0
maxSpeed = 0

# Check if the required number of command-line arguments are provided
if len(sys.argv) != 4:
    print("Usage: python script.py <minSpeed> <maxSpeed> <targetObjectWidth>")
    sys.exit(1)

# Get the values of minSpeed and maxSpeed from command-line arguments
try:
    minSpeed = float(sys.argv[1])
    maxSpeed = float(sys.argv[2])
    Tw = float(sys.argv[3])
except ValueError:
    print("Error: minSpeed and maxSpeed must be numeric values.")
    sys.exit(1)

in1 = 24
in2 = 23
en1 = 25

in3 = 15
in4 = 14
en2 = 18

GPIO.setmode(GPIO.BCM)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en1,GPIO.OUT)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en1,1000)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
p2=GPIO.PWM(en2, 1000)

p.start(minSpeed)
p2.start(minSpeed)

# Function to map a value from one range to another
def map_value(value, from_low, from_high, to_low, to_high):
    return (value - from_low) * (to_high - to_low) / (from_high - from_low) + to_low

# Create the Mask Detection Robot class with the required settings:
class Object_Tracking_Robot:
    def __init__(self):
        # Define HusklyLens settings
        self.husky_lens = HuskyLensLibrary("I2C", "", address=0x32)
        self.is_running = True

        self.cx = 160 # screen x venter
        self.cy = 120 # screen y center
        
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
        if obj is None:
            return False
        
        count=1
        if(type(obj)==list):
            for i in obj:
                print("\t " + ("BLOCK_" if i.type=="BLOCK" else "ARROW_") + str(count) + " : " + json.dumps(i.__dict__))
                self.Ox = json.loads(json.dumps(i.__dict__))["x"]
                self.Oy = json.loads(json.dumps(i.__dict__))["y"]
                self.Ow = json.loads(json.dumps(i.__dict__))["width"]
                count+=1
        else:
            print("\t " + ("BLOCK_" if obj.type=="BLOCK" else "ARROW_") + str(count) + " : " + json.dumps(obj.__dict__))
            self.Ox = json.loads(json.dumps(obj.__dict__))["x"]
            self.Oy = json.loads(json.dumps(obj.__dict__))["y"]
            self.Ow = json.loads(json.dumps(obj.__dict__))["width"]

        return True
            
    def OBJECT_TRACKING(self):
        # Get the recently read block from the HuskyLens
        self.is_running  = self.decodeHuskyLens(self.husky_lens.blocks())

        vx = self.Ox - self.cx
        vy = self.cy - self.Oy

        if abs(vx) < 15:
            vx = 0
        if abs(vy) < 15:
            vy = 0
        
        # mapping
        vxNew = map_value(abs(vx), 0, 160, minSpeed, maxSpeed)
        vyNew = map_value(abs(vy), 0, 120, minSpeed, maxSpeed)

        if vx != 0:
            vxNew = vxNew * (abs(vx)/vx)
        if vy != 0:
            vyNew = vyNew * (abs(vy)/vy)

        if (Tw - self.Ow) > 0:
            if (Tw - self.Ow) > 30:
                vyNew = vyNew + ( (Tw - self.Ow)/2 )
            else:
                vyNew = vyNew + (Tw - self.Ow)

        self.rightMotorSpeed = vyNew - vxNew
        self.leftMotorSpeed = vyNew + vxNew

        self.MOVE_ROBOT()

    def MOVE_ROBOT(self):
        if self.rightMotorSpeed > 0:
            if abs(self.rightMotorSpeed) > maxSpeed:
                self.rightMotorSpeed = maxSpeed
            elif abs(self.rightMotorSpeed) < minSpeed:
                self.rightMotorSpeed = minSpeed
            else:
                self.rightMotorSpeed = abs(self.rightMotorSpeed)

            if self.Ow >= Tw or (not self.is_running):
                self.rightMotorSpeed = 0
                self.leftMotorSpeed = 0
            
            print("rightMotor - forward, Speed: {}".format(self.rightMotorSpeed))
            p.ChangeDutyCycle(self.rightMotorSpeed)
            GPIO.output(in1,GPIO.HIGH)
            GPIO.output(in2,GPIO.LOW)
        else:
            if abs(self.rightMotorSpeed) > maxSpeed:
                self.rightMotorSpeed = maxSpeed
            elif abs(self.rightMotorSpeed) < minSpeed:
                self.rightMotorSpeed = minSpeed
            else:
                self.rightMotorSpeed = abs(self.rightMotorSpeed)

            if self.Ow >= Tw or (not self.is_running):
                self.rightMotorSpeed = 0
                self.leftMotorSpeed = 0

            print("rightMotor - backward , Speed: {}".format(self.rightMotorSpeed))
            p.ChangeDutyCycle(self.rightMotorSpeed)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
        
        if self.leftMotorSpeed > 0:
            if abs(self.leftMotorSpeed) > maxSpeed:
                self.leftMotorSpeed = maxSpeed
            elif abs(self.leftMotorSpeed) < minSpeed:
                self.leftMotorSpeed = minSpeed
            else:
                self.leftMotorSpeed = abs(self.leftMotorSpeed)

            if self.Ow >= Tw or (not self.is_running):
                self.rightMotorSpeed = 0
                self.leftMotorSpeed = 0

            print("leftMotor - forward, Speed: {}".format(self.leftMotorSpeed))
            p2.ChangeDutyCycle(self.leftMotorSpeed)
            GPIO.output(in3,GPIO.HIGH)
            GPIO.output(in4,GPIO.LOW)
        else:
            if abs(self.leftMotorSpeed) > maxSpeed:
                self.leftMotorSpeed = maxSpeed
            elif abs(self.leftMotorSpeed) < minSpeed:
                self.leftMotorSpeed = minSpeed
            else:
                self.leftMotorSpeed = abs(self.leftMotorSpeed)

            if self.Ow >= Tw or (not self.is_running):
                self.rightMotorSpeed = 0
                self.leftMotorSpeed = 0

            print("leftMotor - backward , Speed: {}".format(self.leftMotorSpeed))
            p2.ChangeDutyCycle(self.leftMotorSpeed)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)

# Define a new class object named 'robot':
robot = Object_Tracking_Robot()

while True:
    # Get blocks from the HuskyLens:
    robot.OBJECT_TRACKING()
    # sleep(1)