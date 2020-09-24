from email.mime.text import MIMEText
import smtplib
def send_email(email, height, avg, count):
    from_email = "collectorheight@gmail.com"
    from_password = "heightcollector"
    to_email = email

    subject="height data"
    message="Hey there, your height is <strong>%s</strong>. <br> Average height of <strong>%s</strong> people in our database including you was <i><strong>%s</strong></i>"%(height,count,avg)
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To']=to_email
    msg['From']=from_email
    gmail=smtplib.SMTP('smtp.gmail.com',587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)

    gmail.send_message(msg)