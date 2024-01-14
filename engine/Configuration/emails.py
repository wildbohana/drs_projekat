import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Admin will send email to himself
def sendEmail(subject, body):
    gmail_user = "drs.projekat.tim12@gmail.com"
    gmail_password = "qsxj baol xvdc czlk"  # App password
    to_email = "drs.projekat.tim12@gmail.com"

    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        #server.connect('smtp.gmail.com', 587)
        #server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, message.as_string())

    print("Email sent successfully!")
