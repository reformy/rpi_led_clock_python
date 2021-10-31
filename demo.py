import datetime
import os
from time import sleep

from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219


class LedClock:
    def __init__(self):
        self.on_rpi = os.uname()[1] == 'ledclock'
        self.seg = None

        self.init_spi()

    def init_spi(self):
        if self.on_rpi:
            serial = spi(port=0, device=0, gpio=noop())
            device = max7219(serial, cascaded=2)
            self.seg = sevensegment(device)

    def show(self, text: str):
        if self.on_rpi:
            self.seg.text = f'{text[1]}{text[0]}{text[3]}{text[2]}'
        else:
            print(f'Show: "{text}"')

    @staticmethod
    def str_if_not_zero(n: int) -> str:
        return str(n) if n else ''

    def main(self):
        while True:
            now = datetime.datetime.now()
            h1 = self.str_if_not_zero(now.hour // 10)
            h2 = str(now.hour % 10)
            m1 = str(now.minute // 10)
            m2 = str(now.minute % 10)
            self.show(f'{h1}{h2}{m1}{m2}')
            sleep(1)


if __name__ == '__main__':
    LedClock().main()
