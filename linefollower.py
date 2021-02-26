import RPi.GPIO as IO
import time

TRIG = 23
ECHO = 24
i=0


IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(TRIG,IO.OUT)
IO.setup(ECHO,IO.IN)
IO.output(TRIG, False)
print("Calibrating.....")
time.sleep(0.2)

IO.setup(2,IO.IN) #GPIO 2 -> Left IR out
IO.setup(3,IO.IN) #GPIO 3 -> Right IR out


IO.setup(4,IO.OUT) #GPIO 4 -> Motor 1 terminal A
IO.setup(14,IO.OUT) #GPIO 14 -> Motor 1 terminal B

IO.setup(17,IO.OUT) #GPIO 17 -> Motor Left terminal A
IO.setup(18,IO.OUT) #GPIO 18 -> Motor Left terminal B

print("Hello world")

print("")

print("Starting engine")




while 1:
    
    IO.output(TRIG, True)
    time.sleep(0.00010)
    IO.output(TRIG, False)

    while IO.input(ECHO)==0:
      pulse_start = time.time()

    while IO.input(ECHO)==1:
      pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = pulse_duration * 17150

    distance = round(distance+1.15, 2)
    #print(distance)

    if distance<=20 and distance>=1:
        print ("Object ahead at distance of :",distance,"cm")
        i=1
        IO.output(4,True) #1A+
        IO.output(14,True) #1B-

        IO.output(17,True) #2A+
        IO.output(18,True) #2B-
      
    if distance>20 and i==1:
        print ("No Object detected - Distance - ",distance,"cm")
        print ("Moving/....")
        i=0

    
        if(IO.input(2)==True and IO.input(3)==True): #both while move forward
            print("Moving Forward")
            IO.output(4,True) #1A+
            IO.output(14,False) #1B-

            IO.output(17,True) #2A+
            IO.output(18,False) #2B-

        elif(IO.input(2)==False and IO.input(3)==True): #turn right
            print("Moving Right")
            IO.output(4,True) #1A+
            IO.output(14,True) #1B-

            IO.output(17,True) #2A+
            IO.output(18,False) #2B-

        elif(IO.input(2)==True and IO.input(3)==False): #turn left
            print("Moving Left")
            IO.output(4,True) #1A+
            IO.output(14,False) #1B-

            IO.output(17,True) #2A+
            IO.output(18,True) #2B-

        else:  #stay still
            print("Stopping")
            IO.output(4,True) #1A+
            IO.output(14,True) #1B-

            IO.output(17,True) #2A+
            IO.output(18,True) #2B-
    time.sleep(2)