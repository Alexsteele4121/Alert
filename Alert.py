import smtplib
from email.message import EmailMessage
import imghdr
import threading


class Alert:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.MMS = [
            '@mms.att.net', # at&t/Cricket
            '@tmomail.net', # T-Mobile
            '@vzwpix.com', # Verizon Wireless
            # '@pm.sprint.com', # Sprint
            '@mypixmessages.com', # XFinity
            '@vmpix.com', # Virgin Mobile
            '@msg.fi.google.com', # Google Fi
            '@mmst5.tracfone.com' # Tracfone
        ]

    def SendAlert(self, Receiver: str, Message: str, Subject: str = None, Image: str = None,
                  From: str = None):
        if Receiver.find('@') != -1:
            self.Email(Receiver, Message, Subject, Image, From)
        else:
            self.Text(Receiver, Message, Subject, Image, From)

    def Text(self, Receiver: str, Message: str, Subject: str = None, Image: str = None, From: str = None):
        Messages = []
        for Provider in self.MMS:
            msg = EmailMessage()
            msg['Subject'] = Subject
            msg['From'] = From
            msg['To'] = Receiver + Provider
            msg.set_content(Message)

            if Image:
                with open(Image, 'rb') as f:
                    file_data = f.read()
                    file_type = imghdr.what(f.name)
                    file_name = f.name
                msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
            Messages.append(msg)

        for m in Messages:
            threading.Thread(target=self.Send, args=(m,)).start()

    def Email(self, Receiver: str, Message: str, Subject: str = None, Image: str = None, From: str = None):
        msg = EmailMessage()
        msg['Subject'] = Subject
        msg['From'] = From
        msg['To'] = Receiver
        msg.set_content(Message)

        if Image:
            with open(Image, 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
        threading.Thread(target=self.Send, args=(msg,)).start()

    def Send(self, msg):
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(self.username, self.password)
                smtp.send_message(msg)
            return True
        except Exception as e:
            print(e)
            return False
