import asyncio
from aiosmtpd.controller import Controller
from email.parser import BytesParser
from email.policy import default

class CustomSMTPHandler:
    async def handle_CONNECT(self, server, session, envelope, hostname, port):
        print(f'Connection from {session.peer[0]}')
        return '220 Welcome'

    async def handle_MAIL(self, server, session, envelope, address, mail_options):
        print(f'Mail from {address}')
        return '250 OK'

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        print(f'Recipient {address}')
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        print(f'DATA received')
        # Parse the email content
        email_parser = BytesParser(policy=default)
        email_message = email_parser.parsebytes(envelope.content)

        print(f"From: {email_message['From']}")
        print(f"To: {email_message['To']}")
        print(f"Subject: {email_message['Subject']}")
        print(f"Body:\n{email_message.get_body(preferencelist=('plain', 'html')).get_content()}")
        
        return '250 Message accepted for delivery'

async def main():
    handler = CustomSMTPHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=25)  # Use port 25 for standard SMTP
    controller.start()
    print("SMTP server started on port 25.")
    
    try:
        await asyncio.Event().wait()  # Run forever
    except KeyboardInterrupt:
        controller.stop()

if __name__ == "__main__":
    asyncio.run(main())
