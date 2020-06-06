from time import sleep
from e_drone.drone import *
from e_drone.protocol import *

drone=Drone()
drone.open()

print("Takeoff")
drone.sendTakeOff()
for i in range(1,0,-1):
	print(i)
	sleep(1)

print("Pitch")
drone.sendControlWhile(0,3,0,0,100)
for i in range(1,0,-1):
	print(i)
	sleep(1)
	
print("Go Front 10")
drone.sendControlPosition16(1,0,0,0.5,0,0)
for i in range(1,0,-1):
	print(i)
	sleep(1)

print("Roll")
drone.sendControlWhile(3,0,0,0,100)
for i in range(1,0,-1):
	print(i)
	sleep(1)
	
print("Go Right 10")
drone.sendControlPosition16(0,-1,0,0.5,0,0)
for i in range(1,0,-1):
	print(i)
	sleep(1)

print("Yaw")
drone.sendControlWhile(0,0,75,0,100)
for i in range(1,0,-1):
	print(i)
	sleep(1)

print("Pitch")
drone.sendControlWhile(0,3,0,0,100)
for i in range(1,0,-1):
	print(i)
	sleep(1)
    
print("Go Front 1 meter")
drone.sendControlPosition16(1,0,0,0.5,0,0)
for i in range(1,0,-1):
	print(i)
	sleep(1)    
	
print("Landing")
drone.sendLanding()
for i in range(1,0,-1):
	print(i)
	sleep(1)
	
drone.close()	