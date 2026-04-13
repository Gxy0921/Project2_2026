import smtplib
from email.message import EmailMessage

from_email_addr="1966365398@qq.com"
from_email_pass="yjzkdkgbohgqccdc"
to_email_addr="1935872921@qq.com"

msg=EmailMessage()

body="Hello from respberry Pi"
msg.set_content(body)

msg['From']=from_email_addr
msg['To']=to_email_addr

msg['Subject']='TEST EMAIL'

server=smtplib.SMTP('smtp.qq.com',587)

server.starttls()
server.login(from_email_addr,from_email_pass)

server.send_message(msg)

print('Email sent')

server.quit
