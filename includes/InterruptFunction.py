import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
from includes.firebase import firebase

reader = SimpleMFRC522()

db = firebase.database()
all_users = db.child("student").get()

pwmPin = 17
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 50)
pwm.start(0)

def ScanAttendance() :
    id, text = reader.read()
    
def AutomationDoorAllow() :
    id, text = reader.read()
    permission = "1"
    maskStatus = "ON"
    for student in all_users.each() :
        preRecord_ID = int(student.key())
        print(preRecord_ID)
        if id == preRecord_ID :
            print(permission)
            pwm.ChangeDutyCycle(5)
            time.sleep(5)
            pwm.ChangeDutyCycle(10)
            time.sleep(5)
            pwm.ChangeDutyCycle(0)
            
            dataSend = {
                "maskStatus" : maskStatus,
                "tempVal" : tempVal,
                "permission" : permission
                }
                        
            db.child("student").child(id).set(dataSend)
        else :
            permission = "2"
            print(permission)
            
def AutomationDoorDeny() :
    id, text = reader.read()
    permission = "3"
    maskStatus = "OFF"
    for student in all_users.each() :
        preRecord_ID = int(student.key())
        print(preRecord_ID)
        if id == preRecord_ID :
            print(permission)
            
            dataSend = {
                "maskStatus" : maskStatus,
                "tempVal" : tempVal,
                "permission" : permission
                }
                        
            db.child("student").child(id).set(dataSend)
        else :
            print(permission)
