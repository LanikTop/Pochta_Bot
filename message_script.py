import smtplib
from email.mime.text import MIMEText


def send_message(message, recipient, subject):
    sender = 'russaf05@gmail.com'
    password = 'bfrr kbox wmcc sqzs'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = subject
        server.sendmail(sender, recipient, msg.as_string())
        return 'Письмо успешно отправлено'
    except Exception:
        return 'Произошла ошибка'