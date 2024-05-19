from huskylib import HuskyLensLibrary
import json
from time import sleep
from escpos import *
import RPi.GPIO as GPIO          
import sys

huskyLens = HuskyLensLibrary("I2C","",address=0x32)
huskyLens.algorthim("ALGORITHM_OBJECT_RECOGNITION")

def printObjectNicely(obj):
    count=1
    if(type(obj)==list):
        for i in obj:
            print("\t "+ ("BLOCK_" if i.type=="BLOCK" else "ARROW_")+str(count)+" : "+ json.dumps(i.__dict__))
            count+=1
    else:
        print("\t "+ ("BLOCK_" if obj.type=="BLOCK" else "ARROW_")+str(count)+" : "+ json.dumps(obj.__dict__))

while(True):
    # data=huskyLens.blocks()
    data = huskyLens.requestAll()
    if data == None:
        continue
    printObjectNicely(data)
    
    # x=0
    # for i in data:
    #     x=x+1
    #     print("Face {} data: {}".format(x,i))