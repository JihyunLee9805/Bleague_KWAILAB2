from time import sleep
from e_drone.drone import *
from e_drone.protocol import *

drone=Drone()
drone.open()

print("Takeoff")
drone.sendTakeOff()
for i in range(5,0,-1):
	print(i)
	sleep(1)
	
print("Hovering")
drone.sendControlWhile(0,0,0,0,3600)
for i in range(3,0,-1):
	print(i)
	sleep(1)
	
print("Go Front 1 meter")
drone.sendControlPosition16(10,0,0,5,0,0)
for i in range(5,0,-1):
	print(i)
	sleep(1)
	
print("Go Right 1 meter")
drone.sendControlPosition16(0,-10,0,5,0,0)
for i in range(3,0,-1):
	print(i)
	sleep(1)
	
print("Landing")
drone.sendLanding()
for i in range(3,0,-1):
	print(i)
	sleep(1)
	
drone.close()	