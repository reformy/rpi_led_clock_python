import datetime
import os
import traceback
from time import sleep

import requests

from luma.core.interface.serial import spi, noop
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
from requests import ConnectionError


class LedClock:
    DEBUG = False

    def __init__(self):
        self.on_rpi = os.uname()[1] == 'ledclock' and not self.DEBUG
        self.seg = None
        self.network = True

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
        last_minute_for_btc = -1
        while True:
            now = datetime.datetime.now()
            if now.minute % 20 == 0 and last_minute_for_btc != now.minute:
                last_minute_for_btc = now.minute
                self._show_btc()
            elif not self.network and now.second % 5 == 0:
                self._show_no_network()
                self._show_btc()
            else:
                self._show_time(now)

    def _show_btc(self):
        v = self._get_btc()
        if v == 0:
            return

        if v <= 9999:
            s = str(v).rjust(4, ' ')
            self.show(*s)
            sleep(10)
        else:
            n_digits = len(str(v))
            for i_cycle in range(3):
                for i in range(4):
                    fixed_v = v // (10 ** (n_digits - i - 1))
                    s = ' '*(3 - i) + str(fixed_v)
                    self.show(*s)
                    sleep(0.5)

                for i in range(n_digits - 4):
                    fixed_v = (v // (10 ** (n_digits - i - 5))) % 10000
                    s = str(fixed_v).rjust(4, '0')
                    self.show(*s)
                    sleep(0.5)
                self.show(*'    ')
                sleep(0.5)

    def _show_time(self, now):
        h1 = self.str_if_not_zero(now.hour // 10)
        h2 = str(now.hour % 10)
        m1 = str(now.minute // 10)
        m2 = str(now.minute % 10)
        show_dots = now.second % 2 == 1
        dots_str = '.' if show_dots else ''
        self.show(h1, h2, m1 + dots_str, m2 + dots_str)
        sleep(0.2)

    def _show_no_network(self):
        self.show(*'4 40')
        sleep(1)

    def _get_btc(self) -> int:
        try:
            r = requests.get(url='https://api.coinbase.com/v2/prices/spot?currency=USD')
            v = r.json()['data']['amount']
            self.network = True
            return int(float(v))
        except ConnectionError:
            self.network = False
            return 0
        except Exception:
            traceback.print_exc()
            return 0


if __name__ == '__main__':
    LedClock().main()
