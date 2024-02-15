import RPi.GPIO as GPIO
import time
from includes.firebase import firebase

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#LAMP INITIALIZATION
lampPin = 20
GPIO.setup(lampPin, GPIO.OUT)

#BUZZER INITIALIZATION
buzzerPin = 16
GPIO.setup(buzzerPin, GPIO.OUT)

#PWM INITIALIZATION
pwmPin = 17
GPIO.setup(pwmPin, GPIO.OUT)

db = firebase.database()

def controlButton() :
    lampValue = db.child("controlButton/lamp").get().val()
    buzzerValue = db.child("controlButton/emergencyBuzzer").get().val()
    doorValue = db.child("controlButton/automationDoor").get().val()

    if (lampValue == '1') :
        GPIO.output(lampPin, GPIO.HIGH)
    else :
        GPIO.output(lampPin, GPIO.LOW)
        
    if (buzzerValue == '1') :
        GPIO.output(buzzerPin, GPIO.HIGH)
    else :
        GPIO.output(buzzerPin, GPIO.LOW)
        
    if (doorValue == '1') :
        pwm = GPIO.PWM(pwmPin, 50)
        pwm.start(0)
        pwm.ChangeDutyCycle(5)
        time.sleep(1.3)
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        
        dataSend = {
            "automationDoor" : '5'
            }
            
        db.child("controlButton").update(dataSend)
    elif (doorValue == '0') :
        pwm = GPIO.PWM(pwmPin, 50)
        pwm.start(0)
        pwm.ChangeDutyCycle(10)
        time.sleep(1.3)
        pwm.ChangeDutyCycle(0)
        pwm.stop()
        
        dataSend = {
            "automationDoor" : '10'
            }
            
        db.child("controlButton").update(dataSend)
