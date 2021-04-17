import numpy as np
import cv2
import requests
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUZZER= 16
buzzState = False
GPIO.setup(BUZZER, GPIO.OUT)

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
# cap.set(3,640) # set Width
# cap.set(4,480) # set Height
def sendtoserver(frame):
    imencoded = cv2.imencode(".jpg", frame)[1]
    Image = {'image': ('image.jpg', imencoded.tostring(), 'image/jpeg', {'Expires': '0'})}
    response = requests.post("http://192.168.0.102:8000/upload/", files=Image, timeout=5)
    print(response.json())

    try :
        name = (response.json()["names"])[0]
        print(name)
        if (name == "") or (name == None) :
            print(name)
            
            print("intruder found")
            buzzState = True
            GPIO.output(BUZZER, buzzState)
            time.sleep(5)
            buzzState = not buzzState
    
    except:
        print("no face found")
            
        buzzState = True
        GPIO.output(BUZZER, buzzState)
        time.sleep(5)
        buzzState = not buzzState
        GPIO.output(BUZZER, buzzState)
    
    return response


while True:
    ret, img = cap.read()
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(20, 20)
    )
    roi_color = []
    roi_gray = []
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    if (len(faces)> 0):
        print("sending img to server")
        try:
            sendtoserver(roi_color)
        except:
            print("unable to send img")
    else:
        print("no face found") 
    # cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
    cv2.imshow('video',img)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break
    time.sleep(2)
cap.release()
cv2.destroyAllWindows()

# import cv2

# cap = cv2.VideoCapture(0)

# while(True):
#     # Capture frame-by-frame
#     ret, frame = cap.read()

#     # Our operations on the frame come here
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Display the resulting frame
#     cv2.imshow('frame',gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()