from datetime import datetime
from email.message import EmailMessage
import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import AsyncMessage

class EmlHandler(AsyncMessage):
    def __init__(self):
        super().__init__()
        self.no = 0

    async def handle_message(self, message: EmailMessage):
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.no}.eml"
        with open(filename, 'w') as f:
            f.write(message.as_string())
        print(f"{filename} saved.")
        self.no += 1

def run():
    handler = EmlHandler()
    controller = Controller(handler, hostname='0.0.0.0', port=25)
    controller.start()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()

if __name__ == '__main__':
    run()
