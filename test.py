from huskylib import HuskyLensLibrary

huskyLens = HuskyLensLibrary("I2C","",address=0x32)
huskyLens.algorthim("ALGORITHM_OBJECT_RECOGNITION")
while(True):
    data=huskyLens.blocks()
    x=0
    for i in data:
        x=x+1
        print("Face {} data: {}".format(x,i))