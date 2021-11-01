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

    def show(self, *cs):
        if self.on_rpi:
            self.seg.text = f'{cs[1]*4}{cs[0]*4}{cs[3]*4}{cs[2]*4}'
        else:
            print(f'Show: "{cs}"')

    @staticmethod
    def str_if_not_zero(n: int) -> str:
        return str(n) if n else ' '

    def main(self):
        while True:
            now = datetime.datetime.now()
            h1 = self.str_if_not_zero(now.hour // 10)
            h2 = str(now.hour % 10)
            m1 = str(now.minute // 10)
            m2 = str(now.minute % 10)
            show_dots = now.second % 2 == 1
            dots_str = '.' if show_dots else ''
            self.show(h1, h2, m1 + dots_str, m2 + dots_str)
            sleep(0.2)


if __name__ == '__main__':
    LedClock().main()
