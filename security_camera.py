import smtplib, email, os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

from picamera import PiCamera
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

#*********************************************** GPIO setup *************************************************
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

#*********************************************** Email parameters *************************************************
subject='Security Alert: A motion has been detected'
bodyText="""\
Hi,
A motion has been detected in your room.
Please check the attachement sent from rasperry pi security system.
Regards
AS Tech-Workshop
"""
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=587
USERNAME='kiakaiphua@gmail.com'
PASSWORD='Sneakykk25'
RECIEVER_EMAIL='kiakaiphua@gmail.com'

#*********************************************** Video finename and path *************************************************
filename_part1="surveillance"
file_ext=".mp4"
now = datetime.now()
current_datetime = now.strftime("%d-%m-%Y_%H:%M:%S")
filename=filename_part1+"_"+current_datetime+file_ext
filepath="/home/pi/"


def send_email():
 message=MIMEMultipart()
 message["From"]=USERNAME
 message["To"]=RECIEVER_EMAIL
 message["Subject"]=subject

 message.attach(MIMEText(bodyText, 'plain'))
 attachment=open(filepath+filename, "rb")

 mimeBase=MIMEBase('application','octet-stream')
 mimeBase.set_payload((attachment).read())

 encoders.encode_base64(mimeBase)
 mimeBase.add_header('Content-Disposition', "attachment; filename= " +filename)

 message.attach(mimeBase)
 text=message.as_string()

 session=smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
 session.ehlo()
 session.starttls()
 session.ehlo()

 session.login(USERNAME, PASSWORD)
 session.sendmail(USERNAME, RECIEVER_EMAIL, text)
 session.quit
 print("Email sent")


def capture_video():
 camera.start_preview()
 camera.start_recording('/home/pi/newvideo.h264')
 camera.wait_recording(10)
 camera.stop_recording()
 camera.stop_preview()


def remove_file():
 if os.path.exists("/home/pi/newvideo.h264"):
  os.remove("/home/pi/newvideo.h264")
 else:
  print("file does not exist")

 if os.path.exists(filepath+filename):
  os.remove(filepath+filename)
 else:
  print("file does not exist")


#*************************************************** Initiate pi Camera **************************************************************************
camera=PiCamera()

#*************************************************** Main code for method call ********************************************************************
while True:
 i = GPIO.input(11)
 if i==1:
  print("Motion Detected")
  capture_video()
  sleep(2)
  res=os.system("MP4Box -add /home/pi/newvideo.h264 /home/pi/newvideo.mp4")
  os.system("mv /home/pi/newvideo.mp4 "+filepath+filename)
  send_email()
  sleep(2)
  remove_file()