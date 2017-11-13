
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP, SMTPException

class emailUtility:
    image_fn = 'util/%d.png'
    # image_fn = '/%d.png'


    def __init__(self):
        self.email_server = SMTP('smtp.gmail.com', 587)
        try:
            self.email_server.ehlo()
            self.email_server.starttls()
            self.email_server.ehlo()
            #I have created an email account to work for this account.
            self.email_server.login('klaviyot@gmail.com', 'klaviyoklaviyo')  # app-specific verification code
        except SMTPException as se:
            print('Unable to set up smtp connection, due to:\n' + str(se))
            self.email_server.close()
            return

    def send_email(self):
        m = MIMEMultipart()
        m['from'] = sender
        m['to'] = ws.email
        m['subject'] = subject

    def get_email_header(self, sender, from_user, subject):
        return MIMEMultipart()

    #helper method to attach text to the email message
    def attach_text(self, message, form, image):
        message.attach(MIMEText(form + image, 'html'))
        return message

    # helper method to attach image to the email message
    def attach_image(self, m, image_index):
        image = MIMEImage(open(self.image_fn % image_index, 'rb').read())
        image.add_header('Content-ID', '<weather>')
        m.attach(image)
        return m

    #helper method to send the email using smtp client
    def send_email_to(self, sender, email_dict):
        for e in email_dict.keys():
            try:
                self.email_server.sendmail(sender, (e,), str(email_dict[e]))
                print('email to ' + str(e) + ' sent.')
            except SMTPException as se:
                print('email to ' + str(e) + ' not sent, due to:\n' + str(se))
                continue
        self.email_server.close()
