import RPi.GPIO as IO
import time
IO.setwarnings(False)
IO.setmode(IO.BCM)

IO.setup(3,IO.IN) #GPIO 2 -> Left IR out
IO.setup(5,IO.IN) #GPIO 3 -> Right IR out

IO.setup(7,IO.OUT) #GPIO 4 -> Motor 1 terminal A
IO.setup(8,IO.OUT) #GPIO 14 -> Motor 1 terminal B

IO.setup(11,IO.OUT) #GPIO 17 -> Motor Left terminal A
IO.setup(12,IO.OUT) #GPIO 18 -> Motor Left terminal B

while 1:

    if(IO.input(3)==True and IO.input(5)==True): #both while move forward     
        IO.output(7,True) #1A+
        IO.output(8,False) #1B-

        IO.output(11,True) #2A+
        IO.output(12,False) #2B-

    elif(IO.input(3)==False and IO.input(5)==True): #turn right  
        IO.output(7,True) #1A+
        IO.output(8,True) #1B-

        IO.output(11,True) #2A+
        IO.output(12,False) #2B-

    elif(IO.input(3)==True and IO.input(5)==False): #turn left
        IO.output(7,True) #1A+
        IO.output(8,False) #1B-

        IO.output(11,True) #2A+
        IO.output(12,True) #2B-

    else:  #stay still
        IO.output(7,True) #1A+
        IO.output(8,True) #1B-

        IO.output(11,True) #2A+
        IO.output(12,True) #2B-
        
