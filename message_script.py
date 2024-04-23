import smtplib
from email.mime.base import MIMEBase
import os
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders


def send_message(message, recipient, subject, user):
    sender = 'russaf05@gmail.com'
    password = 'bfrr kbox wmcc sqzs'
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        server.login(sender, password)
        msg = MIMEMultipart()
        msg["Subject"] = subject
        if os.path.isdir(fr'data/user_documents/{user}'):
            for filename in os.listdir(fr'data/user_documents/{user}'):
                f = os.path.join(fr'data/user_documents/{user}', filename)
                if os.path.isfile(f):
                    part = MIMEBase('application', "octet-stream")
                    with open(f, 'rb') as file:
                        part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',
                                    'attachment; filename={}'.format(Path(f).name))
                    msg.attach(part)
        server.sendmail(sender, recipient, msg.as_string())
        return 'Письмо успешно отправлено'
    except Exception as ex:
        print(ex)
        return 'Произошла ошибка'
