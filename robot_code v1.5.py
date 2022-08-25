
import imrt_robot_serial
import signal
import time
import sys
import random


LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 100
TURNING_SPEED = 100
STOP_DISTANCE = 25
COMPENSATION_GAIN = 50
LEFT_MOTOR_COMPENSATION = 0
RIGHT_MOTOR_COMPENSATION = 0
#Egne eksperimnentelle endringer 


# We want our program to send commands at 10 Hz (10 commands per second)
execution_frequency = 10 #Hz
execution_period = 1. / execution_frequency #seconds


# Create motor serial object
motor_serial = imrt_robot_serial.IMRTRobotSerial()


# Open serial port. Exit if serial port cannot be opened
try:
    motor_serial.connect("/dev/ttyACM0")
except:
    print("Could not open port. Is your robot connected?\nExiting program")
    sys.exit()

    
# Start serial receive thread
motor_serial.run()

#sensor 1 (front) is the dominating sensor
# #sensor 2 (right) and 3 (left) are used when sensor 1 meets an obstacle
#sensor 4 (back) is used when sensor 2 and 3 fail, or if there is no opening to either side


def calculate_compensation(dist_2, dist_3, is_left): 
    if is_left: 
        return (dist_3 * abs(dist_2 - dist_3)) / COMPENSATION_GAIN
    else:
        return (dist_2 * abs(dist_2 - dist_3))  / COMPENSATION_GAIN

        
def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)



def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed + LEFT_MOTOR_COMPENSATION, speed + RIGHT_MOTOR_COMPENSATION)
        time.sleep(0.10)

# Definerer handlinger

def turn_robot_random_angle():

    direction = random.choice([-1,1])
    iterations = random.randint(10, 25)
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)


def turn_robot_right():

    direction = 1
    iterations = 19

    for i in range(iterations):
        time.sleep(0.10)
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)


def turn_robot_left():

    direction = -1
    iterations = 19

    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        time.sleep(0.10)

#Kode for at roboten kj�rer rett fram helt til den m�ter et objekt

print('Entering loop. Ctrl+c to terminate')
while not motor_serial.shutdown_now :
    

# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye

    dist_1 = motor_serial.get_dist_1()
    dist_2 = motor_serial.get_dist_2()
    dist_3 = motor_serial.get_dist_3()
    dist_4 = motor_serial.get_dist_4()

    print("Dist 1:", dist_1, " Dist 2:", dist_2, " Dist 3:", dist_3, " dist_4:", dist_4)

    
    LEFT_MOTOR_COMPENSATION = calculate_compensation(dist_2, dist_3, is_left = True)
    RIGHT_MOTOR_COMPENSATION = calculate_compensation(dist_2, dist_3, is_left = False)
 
    
    if dist_1 < STOP_DISTANCE and dist_2 < STOP_DISTANCE and dist_3 < STOP_DISTANCE:
        
        drive_robot(BACKWARDS, 1)
        
    elif dist_1 < STOP_DISTANCE and dist_2 > STOP_DISTANCE and dist_3 < STOP_DISTANCE:
        
        turn_robot_right()
        
    elif dist_1 < STOP_DISTANCE and dist_2 < STOP_DISTANCE and dist_3 > STOP_DISTANCE:
        
        turn_robot_left()
        
    elif dist_1 < STOP_DISTANCE and dist_2 > STOP_DISTANCE and dist_3 > STOP_DISTANCE:
        
        turn_robot_random_angle()
        
    else:
        drive_robot(FORWARDS, 0.1)

        
"""
# Get and print readings from distance sensors
dist_1 = motor_serial.get_dist_1()
dist_2 = motor_serial.get_dist_2()
print("Dist 1:", dist_1, "   Dist 2:", dist_2)
# Check if there is an obstacle in the way
if dist_1 < STOP_DISTANCE or dist_2 < STOP_DISTANCE:
# There is an obstacle in front of the robot
# First let's stop the robot for 1 second
print("Obstacle!")
stop_robot(1)
# Reverse for 0.5 second
drive_robot(BACKWARDS, 0.5)
# Turn random angle
turn_robot_random_angle()

else:
# If there is nothing in front of the robot it continus driving forwards
drive_robot(FORWARDS, 0.1)
"""




# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
