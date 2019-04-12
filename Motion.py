import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from picamera import PiCamera
import time
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import MotionSensor

fromaddr = "from EMAIL"
toaddr = "to EMAIL"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Alert"

body = "MOTION DETECTED! \n"

msg.attach(MIMEText(body, 'plain'))

camera = PiCamera()
PIN = 18
default = 4
pir = MotionSensor(default)
count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(default, GPIO.IN)
GPIO.setup(PIN, GPIO.OUT)

while True:
    if pir.motion_detected:
        print("Motion Detected")
        GPIO.output(PIN, GPIO.HIGH)
        camera.start_preview()
        camera.capture('/home/pi/Desktop/FINAL/sensor_pictures/image'+str(count)+'.png')

        filename1 = "image"+str(count)+".png"
        attachment1 = open("/home/pi/Desktop/FINAL/sensor_pictures/image"+str(count)+".png", "rb")
        part1 = MIMEBase('application', 'octet-stream')
        part1.set_payload((attachment1).read())
        encoders.encode_base64(part1)
        part1.add_header('Content-Disposition', "attachment; filename=%s" % filename1)
        msg.attach(part1)
        count+=1
        
        sleep(.5)
        camera.capture('/home/pi/Desktop/FINAL/sensor_pictures/image'+str(count)+'.png')

        filename2 = "image"+str(count)+".png"
        attachment2 = open("/home/pi/Desktop/FINAL/sensor_pictures/image" + str(count)+".png", "rb")
        part2 = MIMEBase('application', 'octet-stream')
        part2.set_payload((attachment2).read())
        encoders. encode_base64(part2)
        part2.add_header('Content-Disposition', "attachment; filename= %s" % filename2)
        msg.attach(part2)
        count+=1

        sleep(.5)
        camera.capture('/home/pi/Desktop/FINAL/sensor_pictures/image' +str(count)+'.png')

        filename3 = "image"+str(count)+".png"
        attachment3 = open("/home/pi/Desktop/FINAL/sensor_pictures/image"+str(count)+".png", "rb")
        part3 = MIMEBase('application', 'octet-stream')
        part3.set_payload((attachment3).read())
        encoders.encode_base64(part3)
        part3.add_header('Content-Disposition', "attachment; filename= %s" % filename3)
        msg.attach(part3)
        count+=1

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(fromaddr, "password")
        text = msg.as_string()

        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        sleep(default)
    else:
        GPIO.output(PIN,GPIO.LOW)
        sleep(4)


    
