# (c) KoboldTheGreat
# Permission is granted to anyone to use this software for any purpose
#
# Channel mapping:
# 15: id (always 4)
# 0: D
# 1: C
# 2: B
# 3: Button
# 4: A
# 5: Light Sensor (higher is darker)
# 6: Sound Sensor (higher is louder)
# 7: Slider
#

import serial
import time
from subprocess import call
import os
import subprocess

old = 0

while 1:
    ser = serial.Serial("/dev/ttyUSB0", 38400)
    ser.write(b'\x01')
    s = b''\

    #each scratch packet consists of 18 bytes (2 per channel)
    for i in range(18):
        s += ser.read()
        time.sleep(0.001)
    
    #closing the connection seems to work the best
    ser.close()
    
    #get value + channel for every channel byte pair
    for x in range(0, len(s), 2):
        #channel id
        id = (s[x]>>3)-16
        
        #channel value
        val = (s[x] & 7)<<7 | s[x+1]  
        

        #formatting for the looks
        print("%d:%d " % (id, val), end="") 

        #example on how you could use the slider to control your volume
        if id == 7 and abs(val - old) > 3:
            cmd = (["amixer", "-D", "pulse", "sset", "Master", str(val/10.23) + "%"])
            #pipe stdout to /dev/null so it won't show up
            with open(os.devnull, "w") as f:
                subprocess.call(cmd, stdout=f)
            old = val

    print("\n", end="")
