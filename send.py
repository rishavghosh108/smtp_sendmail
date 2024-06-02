import asyncio
from aiosmtpd.controller import Controller
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Receiving message from:', envelope.mail_from)
        print('Message addressed to  :', envelope.rcpt_tos)
        print('Message length        :', len(envelope.content))

        # Create email message
        subject = "Forwarded Email"
        body = "This is a forwarded email."

        msg = MIMEMultipart()
        msg['From'] = envelope.mail_from
        msg['To'] = ', '.join(envelope.rcpt_tos)
        msg['Subject'] = subject
        msg.attach(MIMEText(envelope.content.decode('utf-8'), 'plain'))

        # Send email using the send_email method
        await self.send_email(envelope.mail_from, envelope.rcpt_tos, msg.as_string())

        return '250 OK'

    async def send_email(self, sender_email, receiver_emails, email_content):
        # Load SMTP server credentials from environment variables for security
        smtp_server = 'mail.bengalintituteoftechnology.online'
        smtp_port = 587
        smtp_username = os.getenv('SMTP_USERNAME', 'your_email@bengalintituteoftechnology.online')
        smtp_password = os.getenv('SMTP_PASSWORD', 'your_password')

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_emails, email_content)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=1025)

    try:
        controller.start()
        print("SMTP server started.")
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        controller.stop()
