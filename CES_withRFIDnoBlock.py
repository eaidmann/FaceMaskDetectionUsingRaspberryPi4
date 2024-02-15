# USAGE
# python3 detect_mask_webcam.py

# import the necessary packages
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from mfrc522 import SimpleMFRC522
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import board
import adafruit_mlx90614
import RPi.GPIO as GPIO
from includes.firebase import firebase
from includes.gpioControl import controlButton
from includes.SystemFunction import *

#FIREBASE INITIALIZATION
db = firebase.database()
all_users = db.child("student").get()

#TEMPERATURE SENSOR INITIALIZATION
i2c = board.I2C()
mlx = adafruit_mlx90614.MLX90614(i2c)
bodyTemp = mlx.object_temperature

#LED PIN INITIALIZATION
greenPin = 19
GPIO.setup(greenPin, GPIO.OUT)

redPin = 21
GPIO.setup(redPin, GPIO.OUT)

#RC522 RFID READER INITIALIZATION
reader = SimpleMFRC522()

def detect_and_predict_mask(frame, faceNet, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)

            # add the face and bounding boxes to their respective
            # lists
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detected
    if len(faces) > 0:
        # for faster inference we'll make batch predictions on *all*
        # faces at the same time rather than one-by-one predictions
        # in the above `for` loop
        faces = np.array(faces, dtype="float32")
        preds = maskNet.predict(faces, batch_size=32)

    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
    default="face_detector",
    help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
    default="mask_detector.model",
    help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
    help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector model from disk
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
    "res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=1920)
    bodyTemp = mlx.object_temperature + 5.70
    tempVal = "{:.2f}" .format(bodyTemp)
    
    #GPIO IOT CONTROL MONITORING
    controlButton()
    
    #READ ANY RFID CARD
    id = reader.read_id_no_block()
    print(id)
    
    # detect faces in the frame and determine if they are wearing a
    # face mask or not
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)

    # loop over the detected face locations and their corresponding
    # locations
    for (box, pred) in zip(locs, preds):
        # unpack the bounding box and predictions
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        # determine the class label and color we'll use to draw
        # the bounding box and text
        if mask > withoutMask:
            label = "Mask On. - " + str(tempVal) + "C"
            color = (0, 255, 0)
            maskStatus = "ON"
            colorMask = (0, 255, 0)
            
            if id == None :
                id = reader.read_id_no_block()
            
            if bodyTemp < 37:
                permitStatus = "ALLOW"
                colorPermit = (0, 255, 0)
                colorTemp = (0, 255, 0)
                GPIO.output(greenPin, GPIO.HIGH)
                GPIO.output(redPin, GPIO.LOW)
                
                if id != None :
                    scan_attendance_open(id, maskStatus, tempVal)
            else :
                colorPermit = (0, 0, 255)
                colorTemp = (0, 0, 255)
                GPIO.output(greenPin, GPIO.LOW)
                GPIO.output(redPin, GPIO.HIGH)
                GPIO.output(buzzerPin, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(buzzerPin, GPIO.LOW)
                time.sleep(1)
                   
        else:
            label = "No Mask. - " + str(tempVal) + "C"
            color = (0, 0, 255)
            maskStatus = "OFF"
            permitStatus = "REJECT"
            colorMask = (0, 0, 255)
            colorPermit = (0, 0, 255)
            GPIO.output(greenPin, GPIO.LOW)
            GPIO.output(redPin, GPIO.HIGH)
            
            if bodyTemp < 37.2 :
                colorTemp = (0, 255, 0)
            else :
                colorTemp = (0, 0, 255)
            
            if id == None :
                id = reader.read_id_no_block()
            
            if id != None :
                scan_attendance_close(id, maskStatus, tempVal)
                
        labelTemp ='Temperature Value ...... ' + str(tempVal)
        labelMask = 'Mask Status ...... ' + maskStatus
        labelPerm = 'Permission Status ...... ' + permitStatus
        
        # display the label and bounding box rectangle on the output
        # frame
#         cv2.putText(frame, label, (startX-50, startY - 10),
#             cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        cv2.putText(frame, labelTemp, (10, 800),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, colorTemp, 2)
        
        cv2.putText(frame, labelMask, (10, 700),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, colorMask, 2)
        
        cv2.putText(frame, labelPerm, (10, 600),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, colorPermit, 2)
        
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)

    # show the output frame
    cv2.imshow("Face Mask Detector", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
GPIO.cleanup()