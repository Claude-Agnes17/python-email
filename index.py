import email
from email.contentmanager import raw_data_manager
from email.mime.text import MIMEText
import smtplib
import imaplib

id = input("id : ")
password = input("password : ")
mode = input("send/receive : ")

def send_mail(user, password):
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(id, password)

    to = input("receiver e-mail address : ")
    subject = input("title : ")
    message = input("message : ")

    msg = MIMEText(message)
    msg['Subject'] = subject
    smtp.sendmail(user, to, msg.as_string())
    smtp.quit()


def receive_mail(user, password):
    imap = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    imap.login(user, password)

    imap.select('inbox')

    status, messages = imap.uid('search', None, 'ALL')

    messages = messages[0].split()
    recent_email = messages[-1]

    res, msg = imap.uid('fetch', recent_email, "(RFC822)")

    raw = msg[0][1]

    raw_readable = msg[0][1].decode('utf-8')

    email_message = email.message_from_string(raw_readable)

    if email_message.is_multipart():
        for part in email_message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = email_message.get_payload(decode=True)

    html = open("email.html", "wb")
    html.write(body)
    html.close()
    imap.close()    
    imap.logout()



if mode == 'send':
    send_mail(id, password)
elif mode == 'receive':
    receive_mail(id, password)