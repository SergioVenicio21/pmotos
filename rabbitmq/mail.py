import os
from smtplib import SMTP_SSL

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Environment, FileSystemLoader


class Email:
    def __init__(self):
        self.server = 'smtp.gmail.com'
        self._from = 'sergiovenicio2015@gmail.com'
        self.pwd = 'emsssxnydvlhndqb'

    def load_template(self, template_name):
        env = Environment(loader=FileSystemLoader('templates/emails/'))
        return env.get_template(template_name)

    def load_smtp_client(self):
        smtp_client = SMTP_SSL(self.server, 465)
        smtp_client.login(self._from, self.pwd)

        return smtp_client

    def sendemail(self, to, subject, msg):
        smtp_client = self.load_smtp_client()

        _msg = MIMEMultipart('alternative')
        _msg['Subject'] = subject
        _msg['From'] = self._from

        template = self.load_template('generate_token.html')

        html  = template.render(
            token=msg['token'],
            expire_date=msg['expire_date']
        )

        html = MIMEText(html, 'html')

        _msg.attach(html)

        resp = smtp_client.sendmail(
            self._from,
            to,
            str(_msg)
        )

        smtp_client.close()

        return resp

