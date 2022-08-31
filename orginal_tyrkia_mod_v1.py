# Import some modules that we need
import imrt_robot_serial
import signal
import time
import sys
import random

LEFT = -1
RIGHT = 1
FORWARDS = 1
BACKWARDS = -1
DRIVING_SPEED = 150
TURNING_SPEED = 100
STOP_DISTANCE = 25

def stop_robot(duration):

    iterations = int(duration * 10)
    
    for i in range(iterations):
        motor_serial.send_command(0, 0)
        time.sleep(0.10)



def drive_robot(direction, duration):
    
    speed = DRIVING_SPEED * direction
    iterations = int(duration * 10)

    for i in range(iterations):
        motor_serial.send_command(speed, speed)
        



def turn_robot_random_angle():

    direction = random.choice([-1,1])
    iterations = 19
    
    for i in range(iterations):
        motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
        


def turn_robot_left():
    
    direction = 1
    iterations = 19

    for i in range(iterations):
      motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)


def turn_robot_right():

    direction = -1
    iterations = 19

    for i in range(iterations):
      motor_serial.send_command(TURNING_SPEED * direction, -TURNING_SPEED * direction)
      
	

def Oppretning_hoyre():

    left_gain = 1
    right_gain = 2
    iterations = 4
    for i in range(iterations):
      motor_serial.send_command(TURNING_SPEED * left_gain, TURNING_SPEED * right_gain)
      

def Oppretning_venstre():
     
    left_gain = 2
    right_gain = 1
    iterations = 2
    for i in range(iterations):
      motor_serial.send_command(TURNING_SPEED * left_gain, TURNING_SPEED * right_gain)
      


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


# Now we will enter a loop that will keep looping until the program terminates
# The motor_serial object will inform us when it's time to exit the program
# (say if the program is terminated by the user)
print("Entering loop. Ctrl+c to terminate")
while not motor_serial.shutdown_now :


    ###############################################################
    # This is the start of our loop. Your code goes below.        #
    #                                                             #
    # An example is provided to give you a starting point         #
    # In this example we get the distance readings from each of   #
    # the two distance sensors. Then we multiply each reading     #
    # with a constant gain and use the two resulting numbers      #
    # as commands for each of the two motors.                     #
    #  ________________________________________________________   #
    # |                                                        |  #
    # V                                                           #
    # V                                                           #
    ###############################################################


	#sensor 1 (front) is the dominating sensor
	#sensor 2 (right) and 3 (left) are used when sensor 1 meets an obstacle
	#sensor 4 (back) is used when sensor 2 and 3 fail, or if there is no opening to either side

  dist_1 = motor_serial.get_dist_1() #senor - foran
  dist_2 = motor_serial.get_dist_2() #sensor - venstre
  dist_3 = motor_serial.get_dist_3() #sensor - høyre
  dist_4 = motor_serial.get_dist_4() #sensor - venstre bak

  print("Dist 1:", dist_1, " Dist 2:", dist_2, " Dist 3:", dist_3, " dist_4:", dist_4)


	#Kode for at roboten kjører rett fram helt til den møter et objekt
	
  if dist_1 < STOP_DISTANCE and dist_2 < STOP_DISTANCE and dist_3 < STOP_DISTANCE:
    drive_robot(BACKWARDS, 1)
	
  elif dist_1 < STOP_DISTANCE and dist_2 > STOP_DISTANCE and dist_3 < STOP_DISTANCE:
    turn_robot_right()
	
  elif dist_1 < STOP_DISTANCE and dist_2 < STOP_DISTANCE and dist_3 > STOP_DISTANCE:
    turn_robot_left()
	
  elif dist_1 < STOP_DISTANCE and dist_2 > STOP_DISTANCE and dist_3 > STOP_DISTANCE:
    turn_robot_random_angle()
  
  elif dist_1 > STOP_DISTANCE and dist_2 > dist_4 and abs(dist_2 - dist_4) > 4:
    Oppretning_venstre()
	
  elif dist_1 > STOP_DISTANCE and dist_2 < dist_4 and abs(dist_2 - dist_4) > 4:
    Oppretning_hoyre()
  
  else:
    drive_robot(FORWARDS, 0.1)
		
        
                



    ###############################################################
    #                                                           A #
    #                                                           A #
    # |_________________________________________________________| #
    #                                                             #
    # This is the end of our loop,                                #
    # execution continus at the start of our loop                 #
    ###############################################################
    ###############################################################





# motor_serial has told us that its time to exit
# we have now exited the loop
# It's only polite to say goodbye
print("Goodbye")