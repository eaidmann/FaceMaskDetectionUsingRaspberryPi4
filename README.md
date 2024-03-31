# Face_Mask_Detection
Full Tutorial posted - https://www.tomshardware.com/how-to/raspberry-pi-face-mask-detector

![RaspberryPi Face Mask](https://github.com/carolinedunn/Face_Mask_Detection/blob/main/maskon-maskoff.png)

Full Tutorial posted - https://www.tomshardware.com/how-to/raspberry-pi-face-mask-detector

# Face_Mask_Detection_Using_Raspberry_Pi_4
Based on Tom's Hardware tutorial above, I implement their face mask detection model into my Raspberry Pi 4 for my IOT Classroom Entrance System with Face Mask Detection for my Final Year Project during my study.

# Problem Statements

The current classroom entrance system is manually managed which is cause a lot of trouble in the future. For the small scaling classroom, it is still manageable to manually record the student attendance. But what if the scaling is big and need to handle lot of students at one time, and the lecturers or teachers is out of hand. Therefore, the current issue with the existing system that applied to the classroom is there is no proper record of the number of students entering a classroom, hence will cause trouble if there is an unauthorized student enter the classroom. Take note that sometime there is an issue whereby the student does not attend the class, but their friend helps them sign the provided attendance sheet. This led to a loophole with the current manual system and need to prevent immediately as it is an unhealthy habit done by the student.

Next problem is there is no proper monitoring of students before entering the classroom. As for information, the government had released a detailed step of standard operating procedure (SOP) that need to be followed by an institution who want to held a face-to-face meet or lecture. Hence, if this student doesn’t be checked properly, this will lead to a worst situation incoming if there is a student who is being infected by the Covid-19 virus.

Finally, the personnel who guard the entrance of the classroom can’t track whoever had the permission or without permission to enter the classroom. Hence, this will lead to difficulty in tracing the personnel or student who had the close contact or who bring and spread the diseases into the classroom if there are any cases to occur which the need to trace back the student records.

# Objectives

The problem statement mentioned can be solved by the following objectives:
1. To design a systematic record of the amount of the student’s entrance in a classroom.
2. To design and develop an automated face-mask and temperature detection, as well as automated entrance door of the classroom.
3. To prevent any personnel without permission from entering the classroom.

# Scope / Limitations

This project will be focusing on a classroom environment which the target user is from the student and personnel enter and out from the classroom. A small scaling prototype model is built as replacement of the real-size model, but with the same system functionality, controlled by the Raspberry Pi 4 Model B together with the face mask detection camera. A temperature sensor is used to monitor the temperature of the student before entering the classroom. To avoid unauthorized person entering the classroom, an automation door is proposed to ensure the students or other person is checked before entering the classroom and only a certain person that meet the condition can enter the classroom. These records of the students will finally be saved inside a database.

Before student or any personnel is allowed to enter the classroom, an external Universal Serial Bus (USB) Camera with a face-mask detection being programmed using OpenCV as its image processing will be scanning student and the personnel face to ensure that only student or the personnel with a face-mask is permitted the enter the classroom.

To ensure the safety of the student and the personnel, a MLX90641 Non-contact Infra-red (IR) Temperature Sensor device is used so that the student can scan their temperature before entering the classroom without having to physically touch the device to scan their temperature. This is to avoid the spread of the viruses through environment contact. This temperature sensor will be installed before the automation door to avoid any student or personnel who dodge scanning their temperature from entering the classroom. A monitor will display the suitable information for the students or personnel to show the records obtained.

To record the amount of the student inside a classroom, a RC522 RFID Card Reader is attached in front of the automation door so that any student or personnel authorized the entrance of the classroom can scan their attendance using a RFID card as representation to their matric card and staff card. A unique number of this student and personnel that had scanned their attendance will be save directly to the database that being built using Firebase.

Finally, the automation door connected with a MG996R Servo Motor and an alert buzzer will be installed to warn and barred the unauthorized student or personnel from enter the classroom, and inform the lecturer or anyone in the classroom that there is someone trying to break into the classroom without proper check-up procedure. This will be triggered whenever there is misbehaviour at the entrance of the classroom.

# Hardware Components

There are several hardware components involved throughout the implementation of this system: Raspberry Pi 4 Model B, 5MP Rev 1.3 Raspberry Pi Camera, MLX90614 Infrared Temperature Sensor, RC522 RFID Card Reader, MG996R Servo Motor, 5V Buzzer and 16x2 LCD Display with I2C Module.

# Software Involved

Software also plays an important role alongside the hardware.  The software act as interconnection between hardware devices, and allow them to perform an IoT basis. As part of database management system, the software will be implemented inside a Raspberry Pi to connect it to database server in localhost. The software includes throughout the process of creating this system are as follow:  Raspberry Pi Imager, Raspbian, Python IDLE, Thonny, Laragon, phpMyAdmin, Firebase, and OpenCV.

# General System Flowchart

![image](https://github.com/eaidmann/IOT_Classroom_Entrance_System/assets/59868261/830a4a3b-e19e-4117-ae77-548fd62fb966)


# Result

TBD
