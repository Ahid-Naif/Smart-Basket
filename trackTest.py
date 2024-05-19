from huskylib import HuskyLensLibrary
import json
from time import sleep
from escpos import *
import RPi.GPIO as GPIO          
import sys

huskyLens = HuskyLensLibrary("I2C","",address=0x32)
# huskyLens.algorthim("ALGORITHM_OBJECT_TRACKING")
while(True):
    data=huskyLens.blocks()
    # print(data)
    print(huskyLens.learned)
    print("------")
    print(huskyLens.learned())
    x=0
    # for i in data:
    #     x=x+1
    #     print("Face {} data: {}".format(x,i)