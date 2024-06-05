import asyncio
from aiosmtpd.controller import Controller
from datetime import datetime

class EmlHandler:
    no = 0

    async def handle_DATA(self, server, session, envelope):
        filename = '%s-%d.eml' % (datetime.now().strftime('%Y%m%d%H%M%S'), self.no)
        with open(filename, 'w') as f:
            f.write(envelope.content.decode('utf-8'))
        print('%s saved.' % filename)
        self.no += 1
        return '250 Message accepted for delivery'

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
