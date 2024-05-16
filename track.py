# Web-enabled ML Mask Detection Robot Fines for No Mask w/ Penalty Receipt

# Raspberry Pi 3 Model B+ or 4

# By Kutluhan Aktar

# A prototype to minimize the number of staffs having to interact w/ people
# to notify them wearing masks live streaming while operating.

# For more information:
# https://www.theamplituhedron.com/projects/Web-enabled-ML-Mask-Detection-Robot-Fines-for-No-Mask-w-Penalty-Receipt

from huskylib import HuskyLensLibrary
import json
from time import sleep
import datetime
import string
import random
from subprocess import call
from escpos import *

# Create the Mask Detection Robot class with the required settings:
class Mask_Detection_Robot:
    def __init__(self):
        # Define HusklyLens settings
        self.husky_lens = HuskyLensLibrary("I2C", "", address=0x32)
        self.husky_lens_ID = 0
        # Define the case code - unique for each case.
        self.case_code = "default"
        # Test the communication with the HuskyLens.
        print("First request testing: {}".format(self.husky_lens.knock()))
    
    # Decode the data generated by the HuskyLens.
    def decodeHuskyLens(self, obj):
        count=1
        if(type(obj)==list):
            for i in obj:
                print("\t " + ("BLOCK_" if i.type=="BLOCK" else "ARROW_") + str(count) + " : " + json.dumps(i.__dict__))
                self.husky_lens_ID = json.loads(json.dumps(i.__dict__))["ID"]
                count+=1
        else:
            print("\t " + ("BLOCK_" if obj.type=="BLOCK" else "ARROW_") + str(count) + " : " + json.dumps(obj.__dict__))
            self.husky_lens_ID = json.loads(json.dumps(obj.__dict__))["ID"]
            
    # Generate a unique case code for each detected people without a mask.
    def generate_unique_case_code(self, length):
        letters_and_digits = string.ascii_letters + string.digits
        self.case_code = ''.join(random.choice(letters_and_digits) for i in range(length))
        print("\nCase Code Generated => " + self.case_code)
    
    # Capture people without a mask when detected by the Huskylens.
    def capture_unmasked(self, width, height, case_code, file_path):
        command_capture = "fswebcam -D 2 -S 20 -r " + width + "x" + height + " " + file_path + case_code + ".jpg"
        command_stop_motion = "sudo service motion stop"
        command_start_motion = "sudo service motion start"
        # Take a picture after interrupting the motion module.
        print("\nStatus => Motion Module Interrupted!")
        call([command_stop_motion], shell=True)
        sleep(10)
        print("\nStatus => Fswebcam Module Activated!\n")
        call([command_capture], shell=True)
        sleep(5)
        print("\nStatus => Motion Module Restarted!\n")
        call([command_start_motion], shell=True)
        sleep(5)
        
    # Via the Thermal Printer, print the fine receipt when detecting people without a mask.
    def print_fine_receipt(self, case_code, fine, due):
        print("\nStatus => Printer Working!")
        # Define character design and font sizes for each line.
        command_thermal_printer = []
        command_thermal_printer.append("sudo chmod 666 /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1B\x45\x01' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x42\x01' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x21\x37' > /dev/usb/lp0")
        command_thermal_printer.append("echo '&&&' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x42\x10' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x21\x24\x0a' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'COVID-19' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x21\x12' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Management' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Violation' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Notice' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x21\x01' > /dev/usb/lp0")
        command_thermal_printer.append("echo '\\nReceipt No:' > /dev/usb/lp0")
        command_thermal_printer.append("echo '" + case_code + "\\n' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Issue Date: " + datetime.datetime.now().strftime('%m-%d-%Y') + "' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Time: " + datetime.datetime.now().strftime('%H:%M:%S') + "' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Amount: " + fine + "' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'Due Date: In " + due + " Days\\n' > /dev/usb/lp0")
        command_thermal_printer.append("printf '\x1D\x21\x09' > /dev/usb/lp0")
        command_thermal_printer.append("echo '(!) You comitted' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'a code' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'violation by not' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'wearing a mask' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'in public.\\n' > /dev/usb/lp0")
        command_thermal_printer.append("echo '(!) To inspect the' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'picture showing' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'you not wearing' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'a mask in public' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'and pay the penalty' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'enter your' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'receipt number' > /dev/usb/lp0")
        command_thermal_printer.append("echo 'to this page:\\n' > /dev/usb/lp0")
        
        # Print each line via the serial port.
        for i in range(len(command_thermal_printer)):
            call([command_thermal_printer[i]], shell=True)
            sleep(0.5)
        # Print QR Code w/ Settings
        thermal_printer = printer.File("/dev/usb/lp0")
        thermal_printer.qr("http://" + self.server + "/Mask_Detection_Robot_Dashboard/Payments/?q=" + case_code, size=4, model=2)
        thermal_printer.cut()
        print("\nStatus => Printer Printed the Receipt!\n\n")
          
    def MASK_DETECTION(self):
        # Get the recently read block from the HuskyLens to detect the object ID.
        self.decodeHuskyLens(self.husky_lens.blocks())
        if(self.husky_lens_ID == 1):
            print("ID = " + str(self.husky_lens_ID) + " Status => Masked")
        elif(self.husky_lens_ID == 2):
            print("ID = " + str(self.husky_lens_ID) + " Status => UnMasked")
            # Generate the case code.
            self.generate_unique_case_code(15)
            # Capture people without a mask.
            self.capture_unmasked("640", "480", self.case_code, self.file_location)
            # Print the fine receipt with the penalty.
            self.print_fine_receipt(self.case_code, "$50", "3")
        elif(self.husky_lens_ID == 3):
            print("ID = " + str(self.husky_lens_ID) + " Status => Default")
        

# Define a new class object named 'robot':
robot = Mask_Detection_Robot()

while True:
    # Get blocks from the HuskyLens:
    robot.MASK_DETECTION()
    sleep(2)