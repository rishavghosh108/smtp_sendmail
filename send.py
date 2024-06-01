import smtpd
import asyncore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        # print('Receiving message from:', peer)
        # print('Message addressed from:', mailfrom)
        # print('Message addressed to  :', rcpttos)
        # print('Message length        :', len(data))

        # Create email message
        subject = "Forwarded Email"
        body = "This is a forwarded email."

        msg = MIMEMultipart()
        msg['From'] = mailfrom
        msg['To'] = ', '.join(rcpttos)
        msg['Subject'] = subject
        msg.attach(MIMEText(data, 'plain'))

        # Send email using the send_email method
        self.send_email(mailfrom, rcpttos, msg.as_string())
        return

    def send_email(self, sender_email, receiver_emails, email_content):
        # Load SMTP server credentials from environment variables for security
        smtp_server = os.getenv('SMTP_SERVER', 'mail.bengalintituteoftechnology.online')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        # smtp_username = os.getenv('SMTP_USERNAME', 'your_email@bengalintituteoftechnology.online')
        # smtp_password = os.getenv('SMTP_PASSWORD', 'your_password')

        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            # server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_emails, email_content)
            server.quit()
            print("Email sent successfully")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # Start the custom SMTP server on the specified host and port
    server = CustomSMTPServer(('0.0.0.0', 1025), None)

    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass
