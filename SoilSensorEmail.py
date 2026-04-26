import RPi.GPIO as GPIO
import smtplib
from email.message import EmailMessage
import time
from datetime import datetime

from_email_addr="1966365398@qq.com"
from_email_pass="yjzkdkgbohgqccdc"
to_email_addr="1935872921@qq.com"

channel=4
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel,GPIO.IN)

def send_email_notification(status):
    msg=EmailMessage()
    msg['From']=from_email_addr
    msg['To']=to_email_addr
    msg['Subject']=f"Plant Monitor Report{datetime.now().strftime('%H:%M')}"

    current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body=f"Report Time:{current_time}\nStatus:{status}"
    msg.set_content(body)

    try:
       server=smtplib.SMTP('smtp.qq.com',587)
       server.starttls()
       server.login(from_email_addr,from_email_pass)
       server.send_message(msg)
       server.quit()
       print(f"Email sent succesfully:{status}")
    except Exception as e:
       print(f"Failed to send email:{e}")

def send_startup_email():
    sensor_val=GPIO.input(channel)
    status="Water not needed!"if sensor_val==0 else"Please water your plant!"
    send_email_notification(status)

send_startup_email()

time.sleep(10)

seconds=time.time()
result=time.localtime(seconds)
lastValue=result.tm_hour
print(f"Current Beijing Hour:{lastValue}")

count=0
max_count=4

while count<max_count:
    current_time_struct=time.localtime(time.time())
    Current_Value=current_time_struct.tm_hour

    if (lastValue==Current_Value):
      time.sleep(60)
    else:
      difference=Current_Value-lastValue

      if difference<0:
        difference+=24

      if (difference>=1):
        sensor_reading=GPIO.input(channel)

        if sensor_reading==0:
           status="Water not needed!"
        else:
           status="Please water your plant!"

        send_email_notification(status)

        count+=1
        lastValue=Current_Value

        if count>=max_count:
           break
      else:
        lastValue=Current_Value
        time.sleep(60)

GPIO.cleanup()
