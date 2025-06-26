# Imports go at the top
from microbit import *

i2c.init()

AS5600_ADDRESS = 0x36
ANGLE_REGISTER = b'\x0E'
STATUS_REGISTER = b'\x0b'

section = 360 / 16
def displayAngle(degrees):
    if  (degrees < section) | (degrees > 360 - section):
        display.show(Image.ARROW_N)
    elif (degrees < 90 - section):
        display.show(Image.ARROW_NE)
    elif (degrees < 90 + section):
        display.show(Image.ARROW_E)
    elif (degrees < 180 - section):
        display.show(Image.ARROW_SE)
    elif (degrees < 180 + section):
        display.show(Image.ARROW_S)
    elif (degrees < 270 - section):
        display.show(Image.ARROW_SW)
    elif (degrees < 270 + section):
        display.show(Image.ARROW_W)
    else:
        display.show(Image.ARROW_NW)

# Code in a 'while True:' loop repeats forever
while True:
    sleep(1000)
    scans = i2c.scan()
    if AS5600_ADDRESS in scans: # Check thath AS5600 is online

        # Read Status
        i2c.write(AS5600_ADDRESS, STATUS_REGISTER) # Select status register
        data = i2c.read(AS5600_ADDRESS,1)
        status = data[0]
        print("status :",  bin(status))
        md = (status >> 5) & 1  # Bit 5 : magnet detected
        ml = (status >> 4) & 1  # Bit 4 : magnet too weak
        mh = (status >> 3) & 1  # Bit 3 : magnet too strong
        
        if md:
            print("Magnet detected")
            
            # Read angle
            i2c.write(AS5600_ADDRESS, ANGLE_REGISTER) # Select angle register
            data = i2c.read(AS5600_ADDRESS, 2) # Read on 2 octets
            angle = (data[0] << 8) | data[1] 
            angleInDegrees = angle * 360 / 4096
            
            print("Angle:", angleInDegrees)
            displayAngle(angleInDegrees)
            
        if ml:
            print("Magnet too weak")

            display.show(Image.NO)
            
        if mh:
            print("Magnet too strong")

            display.show(Image.ANGRY)
            
    else:
        print("Sensor not detected")

        display.show(Image.SKULL)
        

        
