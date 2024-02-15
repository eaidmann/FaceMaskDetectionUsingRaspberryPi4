import RPi.GPIO as GPIO
import time
import board
from mfrc522 import SimpleMFRC522
from includes.firebase import firebase

#FIREBASE INITIALIZATION
db = firebase.database()
all_users = db.child("student").get()

#PWM INITIALIZATION
pwmPin = 17
GPIO.setup(pwmPin, GPIO.OUT)

#ACTIVE BUZZER INITIALIZATION
buzzerPin = 16
GPIO.setup(buzzerPin, GPIO.OUT)

#RC522 RFID READER INITIALIZATION
reader = SimpleMFRC522()

#IR SENSOR PIN INITIALIZATION
irPin = 26
GPIO.setup(irPin, GPIO.IN)

#ATTENDANCE SYSTEM FUNCTION
def scan_attendance_open(uid, MaskStatus, TemperatureVal) :
    pwm = GPIO.PWM(pwmPin, 50)
    pwm.start(0)
    
    for student in all_users.each() :
        preRecord_ID = int(student.key())
        print(str(uid) + "=" + str(preRecord_ID) + "?")
        
        if uid == preRecord_ID :
            permission = "ALLOWED"
            pwm.ChangeDutyCycle(5)
            time.sleep(1.3)
            while(GPIO.input(irPin)) :
                pwm.ChangeDutyCycle(0)
            pwm.ChangeDutyCycle(10)
            time.sleep(1.3)
            pwm.stop()
            
            dataSend = {
                "maskStatus" : MaskStatus,
                "tempVal" : TemperatureVal,
                "permission" : permission
                }
            
            db.child("student").child(uid).update(dataSend)
            print("MASUK!!")
            
        else :
            GPIO.output(buzzerPin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzerPin, GPIO.LOW)
            time.sleep(1)
            print("KELUAR!!!")
        
def scan_attendance_close(uid, MaskStatus, TemperatureVal) :
    for student in all_users.each() :
        preRecord_ID = int(student.key())
        
        if uid == preRecord_ID :
            permission = "DENIED"
            maskStatus = "OFF"
                
            dataSend = {
                "maskStatus" : MaskStatus,
                "tempVal" : TemperatureVal,
                "permission" : permission
                }
            
            db.child("student").child(uid).update(dataSend)
            
            print("REJECT!!!")
        else :
            GPIO.output(buzzerPin, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(buzzerPin, GPIO.LOW)
            time.sleep(1)
            
            print("REJECT TERUSSS!!")
